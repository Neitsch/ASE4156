"""
GraphQL definitions for the Trading App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, relay
from .models import Trade
from .models import TradingAccount


# pylint: disable=too-few-public-methods
class GTrade(DjangoObjectType):
    """
    Exposing the whole Trade object to GraphQL
    """
    class Meta(object):
        """
        Meta Model for Trade
        """
        model = Trade
        interfaces = (relay.Node, )


class GTradingAccount(DjangoObjectType):
    """
    Exposing the whole TradingAccount to GraphQL
    """
    class Meta(object):
        """
        Meta Model for TradingAccount
        """
        model = TradingAccount
        interfaces = (relay.Node, )


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
