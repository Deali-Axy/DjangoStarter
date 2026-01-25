from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from apps.billing.entitlements import has_feature, get_limit
from apps.billing.models import (
    Wallet,
    TopUp,
    LedgerEntry,
    Plan,
    Subscription,
    TopUpStatus,
    TopUpChannel,
)


class BillingCoreTestCase(TestCase):
    """
    billing 核心能力测试：
    - 充值成功入账与幂等
    - 当前订阅唯一性约束
    - 权益判断（feature/limit）
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='u1', email='u1@example.com', password='pass1234')

    def test_topup_mark_succeeded_is_idempotent(self):
        wallet = Wallet.objects.create(user=self.user, currency='CNY', balance=Decimal('0.00'))
        topup = TopUp.objects.create(
            user=self.user,
            wallet=wallet,
            amount=Decimal('10.00'),
            currency='CNY',
            status=TopUpStatus.CREATED,
            channel=TopUpChannel.ADMIN,
        )

        ledger1 = topup.mark_succeeded(idempotency_key='k1', reference='admin-test')
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, Decimal('10.00'))
        self.assertEqual(LedgerEntry.objects.count(), 1)
        self.assertEqual(topup.credited_entry_id, ledger1.id)

        ledger2 = topup.mark_succeeded(idempotency_key='k1', reference='admin-test')
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, Decimal('10.00'))
        self.assertEqual(LedgerEntry.objects.count(), 1)
        self.assertEqual(ledger1.id, ledger2.id)

    def test_subscription_current_unique_constraint(self):
        plan = Plan.objects.create(code='pro', name='Pro', price=Decimal('99.00'), currency='CNY')
        Subscription.objects.create(user=self.user, plan=plan, is_current=True)

        with self.assertRaises(IntegrityError):
            Subscription.objects.create(user=self.user, plan=plan, is_current=True)

    def test_entitlements_feature_and_limit(self):
        plan = Plan.objects.create(
            code='business',
            name='Business',
            price=Decimal('199.00'),
            currency='CNY',
            features={'advanced_export': True},
            limits={'projects_max': 10},
        )
        Subscription.objects.create(user=self.user, plan=plan, is_current=True)

        self.assertTrue(has_feature(user_id=self.user.id, feature_key='advanced_export'))
        self.assertFalse(has_feature(user_id=self.user.id, feature_key='non_exist_feature'))
        self.assertEqual(get_limit(user_id=self.user.id, limit_key='projects_max'), 10)
        self.assertEqual(get_limit(user_id=self.user.id, limit_key='non_exist_limit', default=3), 3)

