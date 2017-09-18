"""
GraphQL definitions for the Stocks App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, relay
from .models import DailyStockQuote, Stock


# pylint: disable=too-few-public-methods
class GStock(DjangoObjectType):
    """
    GraphQL representation of a Stock
    """
    class Meta:
        """
        Meta Model for Stock
        """
        model = Stock
        interfaces = (relay.Node, )


class GDailyStockQuote(DjangoObjectType):
    """
    GraphQL representation of a DailyStockQuote
    """
    class Meta:
        """
        Meta Model for DailyStockQuote
        """
        model = DailyStockQuote
        interfaces = (relay.Node, )


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
