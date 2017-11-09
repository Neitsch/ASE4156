'''
Tests Plaid
'''
import datetime
from unittest import mock
import pytest
import authentication.plaid_middleware as PlaidMiddleware
import plaid
from plaid.api.accounts import Balance, Accounts
from plaid.api.transactions import Transactions
from django.test import TestCase


class PlaidTests(TestCase):
    '''
    Testing Paid Wrapper
    '''
    @classmethod
    def setup_class(cls):
        '''Setting up testing'''
        cls._original_init_method = plaid.__init__
        plaid.__init__ = mock.Mock(return_value=None)
        plaid.__call__ = lambda self, request: self.get_response(request)

    @classmethod
    def teardown_class(cls):
        '''Teardown testing'''
        plaid.__init__ = cls._original_init_method

    @mock.patch.object(
        Balance,
        'get',
        mock.MagicMock(return_value={
            'accounts': [
                {
                    'balances': {'available': 1},
                    'subtype': 'not credit card'
                    },
                {
                    'balances': {'available': 10},
                    'subtype': 'credit card'
                    }
                ]
            })
    )
    @pytest.mark.django_db(transaction=True)
    def test_current_balance(self):
        '''
        Testing PlaidMiddleware.PlaidAPI.current_balance()
        '''
        client = plaid.Client(client_id='', secret='', public_key='', environment='')
        user = PlaidMiddleware.PlaidAPI(access_token='', client=client)
        balance = user.current_balance()
        assert balance == -9.0

    @mock.patch.object(
        Accounts,
        'get',
        mock.MagicMock(return_value={
            'accounts': [
                {
                    'name': 'Test Account',
                    },
                {
                    'name': 'Test Account 2',
                    }
                ]
            })
    )
    @pytest.mark.django_db(transaction=True)
    def test_account_name(self):
        '''
        Testing PlaidMiddleware.PlaidAPI.account_name()
        '''
        client = plaid.Client(client_id='', secret='', public_key='', environment='')
        user = PlaidMiddleware.PlaidAPI(access_token='', client=client)
        account_name = user.account_name()
        assert account_name == 'Test Account'

    @mock.patch.object(
        Transactions,
        'get',
        mock.MagicMock(return_value={
            'transactions': [
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=10),
                    'amount': 100,
                    },
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=13),
                    'amount': 1000,
                    }
                ]
            })
    )
    @mock.patch.object(
        Balance,
        'get',
        mock.MagicMock(return_value={
            'accounts': [
                {
                    'balances': {'available': 1},
                    'subtype': 'not credit card'
                    },
                {
                    'balances': {'available': 10},
                    'subtype': 'credit card'
                    }
                ]
            })
    )
    @pytest.mark.django_db(transaction=True)
    def test_historical_data(self):
        '''
        Testing PlaidMiddleware.PlaidAPI.historical_data()
        '''
        client = plaid.Client(client_id='', secret='', public_key='', environment='')
        user = PlaidMiddleware.PlaidAPI(access_token='', client=client)
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        data = user.historical_data(start_date)

        end = datetime.datetime.now().strftime("%Y-%m-%d")
        mock_data = [
            (end, -9.0),
            (
                (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                -109.0
                ),
            (
                (datetime.datetime.now() - datetime.timedelta(days=13)).strftime("%Y-%m-%d"),
                -1109.0
                )
        ]

        assert len(data) == len(mock_data)

        for i in range(0, len(data)):
            assert data[i][0].strftime("%Y-%m-%d") == mock_data[i][0]
            assert data[i][1] == mock_data[i][1]

    @mock.patch.object(
        Transactions,
        'get',
        mock.MagicMock(return_value={
            'transactions': [
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=10),
                    'amount': -150,
                    },
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=13),
                    'amount': 1000,
                    },
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=13),
                    'amount': 125,
                    }
                ]
            })
    )
    @pytest.mark.django_db(transaction=True)
    def test_income(self):
        '''
        Testing PlaidMiddleware.PlaidAPI.income()
        '''
        client = plaid.Client(client_id='', secret='', public_key='', environment='')
        user = PlaidMiddleware.PlaidAPI(access_token='', client=client)
        income = user.income()
        assert income == 1125.0

    @mock.patch.object(
        Transactions,
        'get',
        mock.MagicMock(return_value={
            'transactions': [
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=10),
                    'amount': 120,
                    },
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=13),
                    'amount': 333,
                    },
                {
                    'date': datetime.datetime.now() - datetime.timedelta(days=13),
                    'amount': -333,
                    }
                ]
            })
    )
    @pytest.mark.django_db(transaction=True)
    def test_expenditure(self):
        '''
        Testing PlaidMiddleware.PlaidAPI.expenditure()
        '''
        client = plaid.Client(client_id='', secret='', public_key='', environment='')
        user = PlaidMiddleware.PlaidAPI(access_token='', client=client)
        income = user.expenditure()
        assert income == -333
