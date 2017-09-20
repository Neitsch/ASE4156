"""
GraphQL definitions for the Stocks App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, Argument, List, NonNull, String, relay
from .models import DailyStockQuote, Stock


# pylint: disable=too-few-public-methods
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


class GStock(DjangoObjectType):
    """
    GraphQL representation of a Stock
    """
    quote_in_range = List(GDailyStockQuote, args={'start': Argument(
        NonNull(String)), 'end': Argument(NonNull(String))})

    class Meta:
        """
        Meta Model for Stock
        """
        model = Stock
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_quote_in_range(data, args, _, __):
        """
        Finds the stock quotes for the stock within a time range
        """
        return (DailyStockQuote
                .objects
                .filter(stock_id=data.id)
                .filter(date__gte=args['start'])
                .filter(date__lte=args['end']))


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
