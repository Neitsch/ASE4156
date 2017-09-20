"""
GraphQL definitions for the Stocks App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, relay
import graphene
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


class AddStock(graphene.Mutation):
    """
    AddStock creates a new Stock that is tracked
    """
    class Input:
        """
        Input to create a stock. We only need the ticker.
        """
        ticker = graphene.NonNull(graphene.String)
        name = graphene.NonNull(graphene.String)
    stock = graphene.Field(lambda: GStock)

    @staticmethod
    def mutate(_, args, __, ___):
        """
        Creates a Stock and saves it to the DB
        """
        stock = Stock(
            ticker=args['ticker'],
            name=args['name']
        )
        stock.save()
        return AddStock(stock=stock)


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
