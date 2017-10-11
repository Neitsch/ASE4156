"""
GraphQL definitions for the Stocks App
"""
from graphene_django import DjangoObjectType
from graphene import AbstractType, Argument, Boolean, Field, Float, List, \
    Mutation, NonNull, String, relay
from trading.models import Trade
from .models import DailyStockQuote, InvestmentBucket, \
    InvestmentBucketDescription, InvestmentStockConfiguration, Stock
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


class GInvestmentBucketAttribute(DjangoObjectType):
    """
    GraphQL representation of a InvestmentBucketDescription
    """
    class Meta:
        """
        Meta Model for InvestmentBucketDescription
        """
        model = InvestmentBucketDescription
        interfaces = (relay.Node, )


class GInvestmentBucket(DjangoObjectType):
    """
    GraphQL representation of a InvestmentBucket
    """
    is_owner = Boolean()

    class Meta:
        """
        Meta Model for InvestmentBucket
        """
        model = InvestmentBucket
        interfaces = (relay.Node, )
        only_fields = ('id', 'name', 'public', 'description', 'stocks')

    @staticmethod
    def resolve_is_owner(data, _args, context, _info):
        """
        Returns whether the user ownes the investment bucket
        """
        return data.owner.id == context.user.profile.id


class GInvestmentStockConfiguration(DjangoObjectType):
    """
    GraphQL representation of a InvestmentStockConfiguration
    """
    class Meta:
        """
        Meta Model for InvestmentStockConfiguration
        """
        model = InvestmentStockConfiguration
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


class AddBucket(Mutation):
    """
    Creates a new InvestmentBucket and returns the new bucket
    """
    class Input(object):
        """
        We only need the name of the new bucket to create it
        """
        name = NonNull(String)
        public = NonNull(Boolean)
    bucket = Field(lambda: GInvestmentBucket)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Creates a new InvestmentBucket and saves it to the DB
        """
        bucket = InvestmentBucket(
            name=args['name'],
            public=args['public'],
            owner=context.user.profile,
        )
        bucket.save()
        return AddBucket(bucket=bucket)


class AddStockToBucket(Mutation):
    """
    Adds a new stock to a specific bucket and returns the bucket
    """
    class Input(object):
        """
        We need the ticker, bucket and quantity to create the connection
        """
        ticker = NonNull(String)
        bucket_name = NonNull(String)
        quantity = NonNull(Float)
    bucket = Field(lambda: GInvestmentBucket)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Adds a new stock to a specific bucket
        """
        bucket = InvestmentBucket.objects.get(name=args['bucket_name'])
        if not bucket.owner.id == context.user.profile.id:
            raise Exception("You don't own the bucket!")
        stock = Stock.objects.get(ticker=args['ticker'])
        investment = InvestmentStockConfiguration(
            bucket=bucket,
            stock=stock,
            quantity=args['quantity']
        )
        investment.save()
        bucket.refresh_from_db()
        return AddStockToBucket(bucket=bucket)


class AddAttributeToInvestment(Mutation):
    """
    Adds a description to an Investment Bucket and returns the bucket
    """
    class Input(object):
        """
        We need the description and the bucket as input
        """
        desc = NonNull(String)
        bucket = NonNull(String)
    bucket = Field(lambda: GInvestmentBucket)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Executes the mutation to add the attribute
        """
        bucket = InvestmentBucket.objects.get(name=args['bucket'])
        if not bucket.owner.id == context.user.profile.id:
            raise Exception("You don't own the bucket!")
        attribute = InvestmentBucketDescription(text=args['desc'], bucket=bucket)
        attribute.save()
        bucket.refresh_from_db()
        return AddAttributeToInvestment(bucket=bucket)


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    pass
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
