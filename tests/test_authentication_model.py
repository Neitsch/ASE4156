"""
Tests for authentication models
"""
from unittest import mock
import pytest
from django.contrib.auth.models import User
from authentication.models import UserBank
from plaid.api.accounts import Balance, Accounts
from plaid.api.transactions import Transactions
import plaid
from test_plaid import transactions_side

def setup_module(cls):
    '''Setting up testing'''
    cls.original_init_method = plaid.__init__
    plaid.__init__ = mock.Mock(return_value=None)
    plaid.__call__ = lambda self, request: self.get_response(request)


def teardown_module(cls):
    '''Teardown testing'''
    plaid.__init__ = cls.original_init_method


@pytest.mark.django_db(transaction=True)
def test_profile_default_acc():
    """
    Test default account on profile
    """
    user1 = User.objects.create(username='user1', password="a")
    acct1 = user1.profile.default_acc()
    assert acct1.account_name == 'default'
    user2 = User.objects.create(username='user2', password="a")
    user2.profile.trading_accounts.create(
        account_name="account2"
    )
    acct2 = user2.profile.default_acc()
    assert acct2.account_name == "account2"


@mock.patch.object(
    Balance,
    'get',
    mock.MagicMock(return_value={
        'accounts': [
            {
                'balances': {'available': 1},
                'subtype': 'not credit card'
            },
        ]
    })
)
@pytest.mark.django_db(transaction=True)
def test_user_bank_current_balance():
    """
    Test current balance updates
    """
    user1 = User.objects.create(username='user1', password="a")
    ub1 = UserBank(
        user=user1, item_id="hi", access_token="Bye",
        institution_name="bankofcool", current_balance_field=10,
        account_name_field="coolaccount", income_field=30,
        expenditure_field=5
    )
    ub1.save()
    assert ub1.current_balance(False) == 10
    assert ub1.current_balance() == 1.0


@mock.patch.object(
    Accounts,
    'get',
    mock.MagicMock(return_value={
        'accounts': [
            {
                'name': 'Testes',
            },
        ]
    })
)
@pytest.mark.django_db(transaction=True)
def test_user_bank_account_name():
    """
    Test account name updates
    """
    user1 = User.objects.create(username='user1', password="a")
    ub1 = UserBank(
        user=user1, item_id="hi", access_token="Bye",
        institution_name="bankofcool", current_balance_field=10,
        account_name_field="coolaccount", income_field=30,
        expenditure_field=5
    )
    ub1.save()
    assert ub1.account_name(False) == "coolaccount"
    assert ub1.account_name() == "Testes"


@mock.patch.object(
    Transactions,
    'get',
    mock.MagicMock(side_effect=transactions_side)
)
@pytest.mark.django_db(transaction=True)
def test_user_bank_income():
    """
    Test income updates
    """
    user1 = User.objects.create(username='user1', password="a")
    ub1 = UserBank(
        user=user1, item_id="hi", access_token="Bye",
        institution_name="bankofcool", current_balance_field=10,
        account_name_field="coolaccount", income_field=30,
        expenditure_field=5
    )
    ub1.save()
    assert ub1.income(update=False) == 30
    assert ub1.income(days=13) == 1125.0


@mock.patch.object(
    Transactions,
    'get',
    mock.MagicMock(side_effect=transactions_side)
)
@pytest.mark.django_db(transaction=True)
def test_expenditures():
    """
    Test expenditures updates
    """
    user1 = User.objects.create(username='user1', password="a")
    ub1 = UserBank(
        user=user1, item_id="hi", access_token="Bye",
        institution_name="bankofcool", current_balance_field=10,
        account_name_field="coolaccount", income_field=30,
        expenditure_field=-5
    )
    ub1.save()
    assert ub1.expenditure(update=False) == -5
    assert ub1.expenditure() == -150
