"""
GraphQL definitions for the Authentication App
"""
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene import AbstractType, Argument, Field, List, Mutation, NonNull, \
    String, relay
from trading.models import TradingAccount
from trading.graphql import GTradingAccount
from stocks.graphql import GStock
from stocks.models import Stock
from .models import Profile


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
        only_fields = ('id', 'profile', 'username')
        interfaces = (relay.Node, )


class GProfile(DjangoObjectType):
    """
    GraphQL representation of a Profile
    """
    stock_find = List(
        GStock, args={'text': GStock, args={'text': Argument(NonNull(String))}})

    class Meta(object):
        """
        Meta Model for Profile
        """
        model = Profile
        only_fields = ('id', 'trading_accounts', 'stock_find')

    @staticmethod
    def resolve_stock_find(_self, args, _context, _info):
        """
        Finds a stock given a case insensitive name
        """
        return Stock.objects.filter(name__icontains=args['text'])


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
