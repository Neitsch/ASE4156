"""
GraphQL definitions for the Stocks App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, Argument, Field, List, Mutation, NonNull, \
    String, relay
from trading.models import Trade
from .models import DailyStockQuote, Stock
from .historical import create_new_stock


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
    quote_in_range = NonNull(List(GDailyStockQuote), args={'start': Argument(
        NonNull(String)), 'end': Argument(NonNull(String))})

    class Meta(object):
        """
        Meta Model for Stock
        """
        model = Stock
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_quote_in_range(data, args, _context, _info):
        """
        Finds the stock quotes for the stock within a time range
        """
        return (DailyStockQuote
                .objects
                .filter(stock_id=data.id)
                .filter(date__gte=args['start'])
                .filter(date__lte=args['end'])
                .order_by('date'))

    @staticmethod
    def resolve_trades(stock, _args, context, _info):
        """
        We need to apply permission checks to trades
        """
        return (Trade
                .objects
                .filter(stock_id=stock.id)
                .filter(account__profile_id=context.user.profile.id))


class AddStock(Mutation):
    """
    AddStock creates a new Stock that is tracked
    """
    class Input(object):
        """
        Input to create a stock. We only need the ticker.
        """
        ticker = NonNull(String)
        name = NonNull(String)
    stock = Field(lambda: GStock)

    @staticmethod
    def mutate(_self, args, _context, _info):
        """
        Creates a Stock and saves it to the DB
        """
        return AddStock(stock=create_new_stock(args['ticker'], args['name']))


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
