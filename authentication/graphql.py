"""
GraphQL definitions for the Authentication App
"""
import datetime
import os
from django.contrib.auth.models import User
from graphene import AbstractType, Argument, Field, Float, List, Mutation, \
    NonNull, String, relay
from graphene_django import DjangoObjectType
from trading.models import TradingAccount
from trading.graphql import GTradingAccount
from stocks.graphql import GStock
from stocks.models import Stock
import plaid
from .models import Profile, UserBank

PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
PLAID_ENV = 'sandbox' if os.environ.get('DEBUG') == "TRUE" else 'development'


# pylint: disable=too-few-public-methods
class GUser(DjangoObjectType):
    """
    GraphQL representation of a User
    """
    class Meta(object):
        """
        Meta Model for User. We must make sure to not expose
        the whole usere object
        """
        model = User
        only_fields = ('id', 'profile', 'username', 'userbank')
        interfaces = (relay.Node, )


class GProfile(DjangoObjectType):
    """
    GraphQL representation of a Profile
    """
    stock_find = List(
        GStock, args={'text': Argument(NonNull(String))})

    class Meta(object):
        """
        Meta Model for Profile
        """
        model = Profile
        only_fields = ('id', 'trading_accounts', 'stock_find')
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_stock_find(_self, args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        return Stock.objects.filter(name__icontains=args['text'])


class GUserBank(DjangoObjectType):
    """
    GraphQL representation of a UserBank
    """
    balance = Float()
    income = Float()
    outcome = Float()

    class Meta(object):
        """
        Meta Model for UserBank
        """
        model = UserBank
        only_fields = ('id', 'balance', 'income', 'outcome')
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_balance(data, _args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        balance = client.Accounts.get(data.access_token)['accounts'][0]['balances']['available']
        return float(balance)

    @staticmethod
    def resolve_income(data, _args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        start = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        end = datetime.datetime.now().strftime("%Y-%m-%d")
        response = client.Transactions.get(data.access_token,
                                           start_date=start, end_date=end)
        transactions = response['transactions']
        plus = sum(filter(lambda x: x > 0, [tx['amount'] for tx in transactions]))
        return float(plus)

    @staticmethod
    def resolve_outcome(data, _args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        start = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        end = datetime.datetime.now().strftime("%Y-%m-%d")
        response = client.Transactions.get(data.access_token,
                                           start_date=start, end_date=end)
        transactions = response['transactions']
        plus = sum(filter(lambda x: x < 0, [tx['amount'] for tx in transactions]))
        return float(plus)


# pylint: disable=no-init
class Query(AbstractType):
    """
    Query represents the entry method for a GraphQL request
    """
    viewer = Field(GUser, )

    @staticmethod
    def resolve_viewer(_self, _args, context, _info):
        """
        The viewer represents the current logged in user
        """
        if not context.user.is_authenticated():
            return None
        return context.user
# pylint: enable=no-init


class AddTradingAccount(Mutation):
    """
    AddTradingAccount creates a new TradingAccount for the user
    """
    class Input(object):
        """
        Input to create a trading account. Right now it's only a name.
        """
        name = String()
    account = Field(lambda: GTradingAccount)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Creates a TradingAccount and saves it to the DB
        """
        account = TradingAccount(
            profile=context.user.profile,
            account_name=args['name']
        )
        account.save()
        return AddTradingAccount(account=account)
# pylint: enable=too-few-public-methods
