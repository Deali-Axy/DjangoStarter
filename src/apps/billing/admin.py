from django.contrib import admin, messages
from django.db import transaction
from simple_history.admin import SimpleHistoryAdmin

from .models import Plan, Subscription, Wallet, LedgerEntry, TopUp, TopUpStatus, TopUpChannel


@admin.register(Plan)
class PlanAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'billing_cycle', 'price', 'currency', 'is_active']
    list_display_links = ['id', 'code', 'name']
    search_fields = ['code', 'name']
    list_filter = ['billing_cycle', 'currency', 'is_active']
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted']
    fieldsets = (
        ('套餐', {'fields': ('id', 'code', 'name', 'billing_cycle', 'price', 'currency', 'is_active')}),
        ('权益配置', {'fields': ('limits', 'features')}),
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )


@admin.register(Subscription)
class SubscriptionAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'plan',
        'status',
        'is_current',
        'current_period_start',
        'current_period_end',
        'provider',
    ]
    list_display_links = ['id', 'user', 'plan']
    search_fields = ['user__username', 'user__email', 'provider_subscription_id']
    list_filter = ['status', 'provider', 'is_current', 'plan']
    autocomplete_fields = ['user', 'plan']
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted']
    fieldsets = (
        ('订阅', {'fields': ('id', 'user', 'plan', 'status', 'is_current')}),
        ('周期', {'fields': ('current_period_start', 'current_period_end', 'cancel_at_period_end', 'canceled_time')}),
        ('来源', {'fields': ('provider', 'provider_subscription_id')}),
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @transaction.atomic
    def save_model(self, request, obj: Subscription, form, change: bool) -> None:
        if obj.is_current and obj.user_id:
            Subscription.objects.filter(user_id=obj.user_id, is_current=True).exclude(id=obj.id).update(is_current=False)
        super().save_model(request, obj, form, change)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'currency', 'balance', 'created_time', 'updated_time']
    list_display_links = ['id', 'user', 'currency']
    search_fields = ['user__username', 'user__email', 'currency']
    list_filter = ['currency']
    autocomplete_fields = ['user']
    readonly_fields = ['id', 'balance', 'created_time', 'updated_time', 'is_deleted']
    fieldsets = (
        ('钱包', {'fields': ('id', 'user', 'currency', 'balance')}),
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'direction', 'amount', 'currency', 'reason', 'reference', 'created_time', 'created_by']
    list_display_links = ['id', 'wallet']
    search_fields = ['wallet__user__username', 'wallet__user__email', 'reference', 'idempotency_key']
    list_filter = ['direction', 'reason', 'currency']
    autocomplete_fields = ['wallet', 'created_by']
    readonly_fields = [
        'id',
        'wallet',
        'direction',
        'amount',
        'currency',
        'reason',
        'reference',
        'idempotency_key',
        'created_by',
        'created_time',
        'updated_time',
        'is_deleted',
    ]
    fieldsets = (
        ('分录', {'fields': ('id', 'wallet', 'direction', 'amount', 'currency', 'reason')}),
        ('关联', {'fields': ('reference', 'idempotency_key', 'created_by')}),
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False


@admin.register(TopUp)
class TopUpAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'amount',
        'currency',
        'status',
        'channel',
        'wallet',
        'credited_entry',
        'created_time',
        'succeeded_time',
        'created_by',
    ]
    list_display_links = ['id', 'user']
    search_fields = [
        'user__username',
        'user__email',
        'provider_trade_no',
        'provider_intent_id',
        'idempotency_key',
    ]
    list_filter = ['status', 'channel', 'currency']
    autocomplete_fields = ['user', 'wallet', 'created_by']
    readonly_fields = ['id', 'credited_entry', 'created_time', 'updated_time', 'is_deleted']
    fieldsets = (
        ('充值单', {'fields': ('id', 'user', 'amount', 'currency', 'status', 'channel', 'wallet')}),
        ('外部支付', {'fields': ('provider_intent_id', 'provider_trade_no', 'idempotency_key')}),
        ('入账', {'fields': ('credited_entry', 'succeeded_time', 'failed_reason')}),
        ('通用信息', {'fields': ('created_by', 'created_time', 'updated_time', 'is_deleted')}),
    )
    actions = ['action_mark_succeeded']

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @transaction.atomic
    def save_model(self, request, obj: TopUp, form, change: bool) -> None:
        if obj.channel == '':
            obj.channel = TopUpChannel.ADMIN

        if obj.created_by_id is None and request.user and request.user.is_authenticated:
            obj.created_by = request.user

        if obj.user_id and not obj.wallet_id:
            wallet, _created = Wallet.objects.get_or_create(user_id=obj.user_id, currency=obj.currency)
            obj.wallet = wallet

        super().save_model(request, obj, form, change)

        if obj.status == TopUpStatus.SUCCEEDED and not obj.credited_entry_id:
            obj.mark_succeeded(
                created_by_id=request.user.id if request.user.is_authenticated else None,
                idempotency_key=obj.idempotency_key or f'admin-topup:{obj.id}',
                reference=obj.provider_trade_no or obj.provider_intent_id,
            )

    @admin.action(description='标记为成功并入账（幂等）')
    def action_mark_succeeded(self, request, queryset):
        succeeded = 0
        skipped = 0
        with transaction.atomic():
            for topup in queryset.select_for_update():
                if topup.credited_entry_id:
                    skipped += 1
                    continue
                topup.status = TopUpStatus.SUCCEEDED
                topup.save(update_fields=['status'])
                topup.mark_succeeded(
                    created_by_id=request.user.id if request.user.is_authenticated else None,
                    idempotency_key=topup.idempotency_key or f'admin-topup:{topup.id}',
                    reference=topup.provider_trade_no or topup.provider_intent_id,
                )
                succeeded += 1

        if succeeded:
            messages.success(request, f'已入账 {succeeded} 笔充值单。')
        if skipped:
            messages.info(request, f'已跳过 {skipped} 笔（已入账）。')

