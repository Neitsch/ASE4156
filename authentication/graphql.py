"""
GraphQL definitions for the Authentication App
"""
import datetime
import os
from django.contrib.auth.models import User
from graphene import AbstractType, Argument, Field, Float, List, Mutation, \
    NonNull, ObjectType, String, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from trading.models import TradingAccount
from trading.graphql import GTradingAccount
from stocks.graphql import GInvestmentBucket, GStock
from stocks.models import InvestmentBucket, Stock
import plaid
import django_filters
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


class GInvestmentBucketFilter(django_filters.FilterSet):
    """
    Filterset to exclude private buckets
    """
    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = kwargs['queryset'].filter(public=True)
        super(GInvestmentBucketFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = InvestmentBucket
        fields = []


class GProfile(DjangoObjectType):
    """
    GraphQL representation of a Profile
    """
    stock_find = List(
        GStock, args={'text': Argument(NonNull(String))})
    invest_suggestions = DjangoFilterConnectionField(
        GInvestmentBucket,
        filterset_class=GInvestmentBucketFilter,
    )

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


class DataPoint(object):
    """
    Dummy class to represent a date / value DataPoint
    """
    def __init__(self, date, value):
        self.date = date
        self.value = value


class GDataPoint(ObjectType):
    """
    GraphQL definition of the DataPoint above
    """
    date = String()
    value = Float()


class GUserBank(DjangoObjectType):
    """
    GraphQL representation of a UserBank
    """
    balance = Float()
    income = Float()
    name = String()
    outcome = Float()
    history = List(GDataPoint, args={'start': Argument(NonNull(String))})

    class Meta(object):
        """
        Meta Model for UserBank
        """
        model = UserBank
        only_fields = ('id', 'balance', 'income', 'outcome')
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_history(data, args, _context, _info):
        """
        Builds the financial history for the user
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        start = args['start']
        end = datetime.datetime.now().strftime("%Y-%m-%d")
        response = client.Transactions.get(data.access_token,
                                           start_date=start, end_date=end)
        transactions = response['transactions']
        value = GUserBank.resolve_balance(data, {}, None, None)
        value_list = [DataPoint(end, value)]
        for transaction in transactions:
            value = value - transaction['amount']
            if not value_list[-1].date == transaction['date']:
                value_list.append(DataPoint(transaction['date'], value))
        return value_list

    @staticmethod
    def resolve_balance(data, _args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        balances = client.Accounts.balance.get(data.access_token)['accounts']
        print(balances)
        extracted_balances = [
            (b['balances']['available']
             if b['balances']['available'] is not None
             else b['balances']['current'])
            for b in balances
        ]
        print(extracted_balances)
        balance = sum(extracted_balances)
        return float(balance)

    @staticmethod
    def resolve_name(data, _args, _context, _info):
        """
        Returns the name of the bank account
        """
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        name = client.Accounts.get(data.access_token)['accounts'][0]['name']
        return name

    @staticmethod
    def resolve_income(data, _args, _context, _info):
        """
        Calculates the income a user has per month
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
        Calculates the expenses a user has
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
