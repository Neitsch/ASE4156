"""
GraphQL definitions for the Authentication App
"""
from django.contrib.auth.models import User
from graphene import Argument, Field, Float, Int, List, Mutation, \
    NonNull, String, relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from trading.models import TradingAccount
from trading.graphql import GTradingAccount
from stocks.graphql import GInvestmentBucket, GStock, GDataPoint, DataPoint
from stocks.models import InvestmentBucket, Stock
from .models import Profile, UserBank


# pylint: disable=too-few-public-methods
class GUser(DjangoObjectType):
    """
    This is the GraphQL representation of a User object. This should *only* be
    accessible for the user himself. It wraps the Django User class.
    """

    class Meta(object):
        """
        Meta Model for User. Most important to note is the fields we expose:
        ID, Profile, Username and UserBank
        """
        model = User
        only_fields = ('id', 'profile', 'username', 'userbank')
        interfaces = (relay.Node, )


class GProfile(DjangoObjectType):
    """
    This is the GraphQL representation of a User Profile. This is more of a
    publically accessible object. Even though we won't expose everything, this
    object allows us to add more fields to the user object.
    """
    stock_find = List(
        NonNull(GStock),
        args={'text': Argument(NonNull(String)),
              'first': Argument(Int)})
    invest_suggestions = DjangoConnectionField(GInvestmentBucket, )
    selected_acc = NonNull(GTradingAccount)

    class Meta(object):
        """
        Meta Model for Profile. We have edges to the Trading Accounts the User
        has, a field that is the current Trading Account a User has, and a
        function that allows the user to search for stocks.
        """
        model = Profile
        only_fields = ('id', 'trading_accounts', 'selected_acc', 'stock_find')
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_stock_find(_self, _info, text, first=None, **_args):
        """
        Finds a stock given a case insensitive name

        :param text: The text the user want to search for.
        :type name: str.
        :param first: The maximum number of results to return
        :type name: int.
        :returns:  QuerySet.
        """
        if first:
            return Stock.find_stock(text, first)
        return Stock.find_stock(text)

    @staticmethod
    def resolve_invest_suggestions(_data, info, **_args):
        """
        Returns a list of buckets that the User can invest in.

        :param info: Information about the user to check which recommendations
            are best for the user.
        :type info: Graphene Request Info.
        :returns:  QuerySet.
        """
        return InvestmentBucket.accessible_buckets(info.context.user.profile)

    @staticmethod
    def resolve_selected_acc(data, _info, **_args):
        """
        Returns the current account the user has selected. Right now it just
        calls the default account of the profile.

        :returns:  QuerySet.
        """
        return data.default_acc()


class GUserBank(DjangoObjectType):
    """
    GraphQL wrapper around the UserBank model. This should *only* be accessible
    to the user
    """
    balance = NonNull(Float)
    income = NonNull(Float)
    name = NonNull(String)
    outcome = NonNull(Float)
    history = NonNull(
        List(NonNull(GDataPoint)), args={'start': Argument(NonNull(String))})

    class Meta(object):
        """
        Meta Model for UserBank
        """
        model = UserBank
        only_fields = ('id', 'balance', 'income', 'outcome')
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_history(data, _info, start, **_args):
        """
        Builds the financial history for the user
        """
        return [
            DataPoint(date, value)
            for (date, value) in data.historical_data(start)
        ]

    @staticmethod
    def resolve_balance(data, _info, **_args):
        """
        Finds the current balance of the user
        """
        return data.current_balance(False)

    @staticmethod
    def resolve_name(data, _info, **_args):
        """
        Returns the name of the bank account
        """
        return data.account_name(False)

    @staticmethod
    def resolve_income(data, _info, **_args):
        """
        Returns the income a user has per month
        """
        return data.income(False)

    @staticmethod
    def resolve_outcome(data, _info, **_args):
        """
        Returns the expenditures a user has per month
        """
        return data.expenditure(False)


# pylint: disable=no-init
class Query(object):
    """
    Query represents the entry method for a GraphQL request
    """
    viewer = Field(GUser, )

    @staticmethod
    def resolve_viewer(_self, info, **_args):
        """
        The viewer represents the current logged in user
        """
        if not info.context.user.is_authenticated():
            return None
        return info.context.user


# pylint: enable=no-init


class AddTradingAccount(Mutation):
    """
    AddTradingAccount creates a new TradingAccount for the user
    """

    class Arguments(object):
        """
        Arguments to create a trading account. Right now it's only a name.
        """
        name = String()

    account = Field(lambda: GTradingAccount)

    @staticmethod
    def mutate(_self, info, name, **_args):
        """
        Creates a TradingAccount and saves it to the DB
        """
        account = TradingAccount(
            profile=info.context.user.profile, account_name=name)
        account.save()
        return AddTradingAccount(account=account)


# pylint: enable=too-few-public-methods
