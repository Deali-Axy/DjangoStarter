from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from simple_history.models import HistoricalRecords

from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class BillingCycle(models.TextChoices):
    """
    订阅计费周期。

    在多数 SaaS 中：
    - 月付：默认入口，转化率更高
    - 年付：提供折扣，提升现金流与留存
    """

    MONTH = 'month', '按月'
    YEAR = 'year', '按年'


class SubscriptionStatus(models.TextChoices):
    """
    订阅状态机（MVP）。

    说明：
    - trialing：试用期
    - active：生效中
    - past_due：扣费失败/欠费（后续接 Stripe 才会频繁出现）
    - canceled：用户/管理员取消（可能仍在当期有效）
    - expired：已失效（周期结束）
    """

    TRIALING = 'trialing', '试用中'
    ACTIVE = 'active', '生效中'
    PAST_DUE = 'past_due', '欠费'
    CANCELED = 'canceled', '已取消'
    EXPIRED = 'expired', '已失效'


class SubscriptionProvider(models.TextChoices):
    """
    订阅来源。

    早期版本支持后台手动开通/变更；
    后续接入 Stripe/支付宝时，用于对账与排障。
    """

    ADMIN = 'admin', '后台开通'
    STRIPE = 'stripe', 'Stripe'
    ALIPAY = 'alipay', '支付宝'


class TopUpStatus(models.TextChoices):
    """
    充值单状态机（MVP）。

    created：已创建，尚未发起支付
    pending：已发起支付，等待回调确认
    succeeded：支付成功，已入账
    failed：失败
    canceled：取消
    refunded：已退款（会产生反向分录）
    """

    CREATED = 'created', '已创建'
    PENDING = 'pending', '支付中'
    SUCCEEDED = 'succeeded', '已成功'
    FAILED = 'failed', '失败'
    CANCELED = 'canceled', '已取消'
    REFUNDED = 'refunded', '已退款'


class TopUpChannel(models.TextChoices):
    """
    充值渠道。

    早期版本主要用 ADMIN 形成可追溯的充值记录；
    后续 Stripe/支付宝接入后，用于区分回调验签与对账口径。
    """

    ADMIN = 'admin', '后台充值'
    STRIPE = 'stripe', 'Stripe'
    ALIPAY = 'alipay', '支付宝'


class LedgerDirection(models.TextChoices):
    """
    账本分录方向。

    - credit：入账（余额增加）
    - debit：出账（余额减少）
    """

    CREDIT = 'credit', '入账'
    DEBIT = 'debit', '出账'


class LedgerReason(models.TextChoices):
    """
    分录原因（MVP）。

    说明：
    - topup：用户充值（或后台充值）入账
    - grant：管理员赠送/补偿
    - consume：按量扣费（后续与用量系统打通）
    - refund：退款/撤销（反向分录）
    - adjust：人工调整（谨慎使用）
    """

    TOPUP = 'topup', '充值入账'
    GRANT = 'grant', '赠送/补偿'
    CONSUME = 'consume', '使用扣费'
    REFUND = 'refund', '退款/撤销'
    ADJUST = 'adjust', '人工调整'


class Plan(ModelExt):
    """
    套餐（VIP/订阅计划）。

    设计要点：
    - limits：配额类（数量/容量/次数），通常用整数
    - features：功能开关类（是否可用某功能），通常用 bool
    """

    code = models.SlugField('套餐代码', max_length=50, unique=True)
    name = models.CharField('套餐名称', max_length=100)
    billing_cycle = models.CharField(
        '计费周期',
        max_length=10,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTH,
    )
    price = models.DecimalField('价格', max_digits=18, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField('币种', max_length=10, default='CNY')
    is_active = models.BooleanField('是否上架', default=True)
    limits = models.JSONField('配额/限制', default=dict, blank=True)
    features = models.JSONField('功能开关', default=dict, blank=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.name}({self.code})'

    class Meta:
        db_table = table_name_wrapper('billing_plan')
        verbose_name = '套餐'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Subscription(ModelExt):
    """
    用户订阅（VIP 实例）。

    说明：
    - MVP 阶段默认一个用户只有一个“当前订阅”（is_current=True）
    - 后续支持升级/降级/历史订阅时，可以 is_current 标记当前，历史保留
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='billing_subscriptions',
        verbose_name='用户',
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='套餐',
    )
    status = models.CharField(
        '状态',
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE,
    )
    provider = models.CharField(
        '来源',
        max_length=20,
        choices=SubscriptionProvider.choices,
        default=SubscriptionProvider.ADMIN,
    )
    provider_subscription_id = models.CharField('外部订阅ID', max_length=200, blank=True, default='')

    current_period_start = models.DateTimeField('本期开始时间', null=True, blank=True)
    current_period_end = models.DateTimeField('本期结束时间', null=True, blank=True)
    cancel_at_period_end = models.BooleanField('到期取消', default=False)
    canceled_time = models.DateTimeField('取消时间', null=True, blank=True)

    is_current = models.BooleanField('是否当前订阅', default=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.user_id} - {self.plan.code} - {self.status}'

    class Meta:
        db_table = table_name_wrapper('billing_subscription')
        verbose_name = '订阅'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_current=True),
                name='uniq_current_subscription_per_user',
            ),
        ]


class Wallet(ModelExt):
    """
    钱包（按币种维度）。

    balance 字段用于快速展示；真实口径以 LedgerEntry 汇总为准（后续可增加对账脚本）。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='billing_wallets',
        verbose_name='用户',
    )
    currency = models.CharField('币种', max_length=10, default='CNY')
    balance = models.DecimalField('余额', max_digits=18, decimal_places=2, default=Decimal('0.00'))

    def __str__(self) -> str:
        return f'{self.user_id}-{self.currency}'

    class Meta:
        db_table = table_name_wrapper('billing_wallet')
        verbose_name = '钱包'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'currency'], name='uniq_wallet_user_currency'),
        ]


class LedgerEntry(ModelExt):
    """
    账本分录。

    核心原则：
    - 分录应尽量“只增不改”，通过追加反向分录表达退款/冲正
    - 对外部系统回调要做幂等（idempotency_key / 外部流水号）
    """

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='ledger_entries',
        verbose_name='钱包',
    )
    direction = models.CharField('方向', max_length=10, choices=LedgerDirection.choices)
    amount = models.DecimalField('金额', max_digits=18, decimal_places=2)
    currency = models.CharField('币种', max_length=10, default='CNY')
    reason = models.CharField('原因', max_length=20, choices=LedgerReason.choices)

    reference = models.CharField('关联引用', max_length=200, blank=True, default='')
    idempotency_key = models.CharField('幂等键', max_length=200, blank=True, default='')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='billing_created_ledger_entries',
        null=True,
        blank=True,
        verbose_name='创建人',
    )

    def __str__(self) -> str:
        return f'{self.wallet_id} {self.direction} {self.amount} {self.currency}'

    class Meta:
        db_table = table_name_wrapper('billing_ledger_entry')
        verbose_name = '账本分录'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            models.Index(fields=['wallet', 'created_time']),
            models.Index(fields=['reason', 'created_time']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['wallet', 'idempotency_key'],
                condition=~Q(idempotency_key=''),
                name='uniq_ledger_wallet_idempotency_key',
            ),
        ]


class TopUp(ModelExt):
    """
    充值单（充值记录）。

    说明：
    - 充值成功后会写入一条 LedgerEntry（credited_entry），保证“入账”可追溯且可幂等
    - 后续接入 Stripe/支付宝时，可通过 provider_intent_id/provider_trade_no 做对账
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='billing_topups',
        verbose_name='用户',
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='topups',
        verbose_name='钱包',
    )
    amount = models.DecimalField('充值金额', max_digits=18, decimal_places=2)
    currency = models.CharField('币种', max_length=10, default='CNY')

    status = models.CharField('状态', max_length=20, choices=TopUpStatus.choices, default=TopUpStatus.CREATED)
    channel = models.CharField('渠道', max_length=20, choices=TopUpChannel.choices, default=TopUpChannel.ADMIN)

    provider_intent_id = models.CharField('外部支付意图ID', max_length=200, blank=True, default='')
    provider_trade_no = models.CharField('外部交易号', max_length=200, blank=True, default='')
    idempotency_key = models.CharField('幂等键', max_length=200, blank=True, default='')

    credited_entry = models.OneToOneField(
        LedgerEntry,
        on_delete=models.PROTECT,
        related_name='credited_topup',
        null=True,
        blank=True,
        verbose_name='入账分录',
    )

    succeeded_time = models.DateTimeField('成功时间', null=True, blank=True)
    failed_reason = models.CharField('失败原因', max_length=500, blank=True, default='')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='billing_created_topups',
        null=True,
        blank=True,
        verbose_name='创建人',
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'{self.user_id} {self.amount} {self.currency} {self.status}'

    @transaction.atomic
    def mark_succeeded(
        self,
        *,
        created_by_id: int | None = None,
        idempotency_key: str = '',
        reference: str = '',
    ) -> LedgerEntry:
        """
        将充值单标记为成功并入账（幂等）。

        参数：
        - created_by_id：后台充值时记录操作人；支付回调时可为空
        - idempotency_key：用于防止重复入账
        - reference：便于对账排障的关联引用（如外部支付单号）
        """

        if self.credited_entry_id:
            return self.credited_entry

        if self.status == TopUpStatus.SUCCEEDED:
            self.succeeded_time = self.succeeded_time or timezone.now()
        else:
            self.status = TopUpStatus.SUCCEEDED
            self.succeeded_time = timezone.now()

        if idempotency_key:
            self.idempotency_key = idempotency_key

        if not self.wallet_id:
            raise ValueError('TopUp.wallet 不能为空')

        ledger = LedgerEntry.objects.create(
            wallet_id=self.wallet_id,
            direction=LedgerDirection.CREDIT,
            amount=self.amount,
            currency=self.currency,
            reason=LedgerReason.TOPUP,
            reference=reference,
            idempotency_key=idempotency_key,
            created_by_id=created_by_id,
        )

        self.credited_entry = ledger
        self.save(update_fields=['status', 'succeeded_time', 'idempotency_key', 'credited_entry'])

        Wallet.objects.filter(id=self.wallet_id).update(balance=models.F('balance') + self.amount)
        return ledger

    class Meta:
        db_table = table_name_wrapper('billing_topup')
        verbose_name = '充值单'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            models.Index(fields=['user', 'created_time']),
            models.Index(fields=['status', 'created_time']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['channel', 'provider_trade_no'],
                condition=~Q(provider_trade_no=''),
                name='uniq_topup_channel_provider_trade_no',
            ),
            models.UniqueConstraint(
                fields=['channel', 'provider_intent_id'],
                condition=~Q(provider_intent_id=''),
                name='uniq_topup_channel_provider_intent_id',
            ),
        ]
