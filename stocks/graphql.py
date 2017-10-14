"""
GraphQL definitions for the Stocks App
"""
from datetime import datetime
from django.db.models import Q
from django.db import transaction
from graphene_django import DjangoObjectType
from graphene import AbstractType, Argument, Boolean, Field, Float, ID, \
    InputObjectType, List, Mutation, NonNull, String, relay
from graphql_relay.node.node import from_global_id
from trading.models import Trade
from .models import DailyStockQuote, InvestmentBucket, \
    InvestmentBucketDescription, InvestmentStockConfiguration, Stock
from .historical import create_new_stock


# pylint: disable=too-few-public-methods
class GInvestmentBucketConfigurationUpdate(InputObjectType):
    """
    Represents one choice of stock for a bucket
    """
    id_value = ID()
    quantity = Float()


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
        only_fields = ('id', 'name', 'public', 'description', 'stocks', 'available')

    @staticmethod
    def resolve_is_owner(data, _args, context, _info):
        """
        Returns whether the user ownes the investment bucket
        """
        return data.owner.id == context.user.profile.id

    @staticmethod
    def resolve_stocks(data, _args, _context, _info):
        """
        Returns the *current* stocks in the bucket
        """
        return data.stocks.filter(end=None)


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
    latest_quote = Field(GDailyStockQuote)

    class Meta(object):
        """
        Meta Model for Stock
        """
        model = Stock
        interfaces = (relay.Node, )

    @staticmethod
    def resolve_latest_quote(data, _args, _context, _info):
        """
        Returns the most recent stock quote
        """
        quote_query = (DailyStockQuote
                       .objects
                       .filter(stock_id=data.id)
                       .order_by('date'))
        if quote_query.count() > 0:
            return quote_query[0]
        return None

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
        is_good = NonNull(Boolean)
    bucket_attr = Field(lambda: GInvestmentBucketAttribute)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Executes the mutation to add the attribute
        """
        bucket = InvestmentBucket.objects.get(
            name=args['bucket'],
            owner__id=context.user.profile.id,
        )
        if not bucket or (not bucket.owner.id == context.user.profile.id):
            raise Exception("You don't own the bucket!")
        attribute = InvestmentBucketDescription(
            text=args['desc'],
            bucket=bucket,
            is_good=args['is_good'],
        )
        attribute.save()
        return AddAttributeToInvestment(bucket_attr=attribute)


class EditAttribute(Mutation):
    """
    Allows to edit an attribute description
    """
    class Input(object):
        """
        Description and ID for the mutation
        """
        desc = NonNull(String)
        id_value = NonNull(ID)
    bucket_attr = Field(lambda: GInvestmentBucketAttribute)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Executes the mutation to change the attribute
        """
        bucket_attr = InvestmentBucketDescription.objects.get(
            id=from_global_id(args['id'])[1],
            bucket__owner__id=context.user.profile.id,
        )
        if not bucket_attr:
            raise Exception("You don't own the bucket!")
        bucket_attr.text = args['desc']
        bucket_attr.save()
        return EditAttribute(bucket_attr=bucket_attr)


class DeleteAttribute(Mutation):
    """
    Deletes an attribute from a bucket
    """
    class Input(object):
        """
        We just need the ID to delete it
        """
        id_value = NonNull(ID)
    is_ok = Field(lambda: Boolean)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        Executes the mutation by deleting the attribute
        """
        bucket_attr = InvestmentBucketDescription.objects.get(
            id=from_global_id(args['id_value'])[1],
            bucket__owner__id=context.user.profile.id,
        )
        if not bucket_attr:
            raise Exception("You don't own the bucket!")
        bucket_attr.delete()
        return DeleteAttribute(is_ok=True)


class EditConfiguration(Mutation):
    """
    Mutation to change the stock configuration of a bucket
    """
    class Input(object):
        """
        As input we take the new configuration and the bucket id
        """
        config = NonNull(List(GInvestmentBucketConfigurationUpdate))
        id_value = NonNull(ID)
    bucket = Field(lambda: GInvestmentBucket)

    @staticmethod
    def mutate(_self, args, context, _info):
        """
        This performs the actual mutation by removing the old configuration and
        then writing the new one
        """
        bucket = InvestmentBucket.objects.get(
            id=from_global_id(args['id_value'])[1],
            owner=context.user.profile,
        )
        with transaction.atomic():
            configs = InvestmentStockConfiguration.objects.filter(
                bucket=bucket,
                end=None,
            ).all()
            for config in configs:
                quote_query = DailyStockQuote.objects.filter(
                    stock__id=config.stock_id
                )
                quote = quote_query.order_by('date')[0]
                bucket.available = (
                    bucket.available +
                    quote.value *
                    config.quantity
                )

            InvestmentStockConfiguration.objects.filter(
                bucket=bucket,
                end=None,
            ).update(end=datetime.now())

            new_configs = []
            for new_config in args['config']:
                quote = DailyStockQuote.objects.filter(
                    stock__id=from_global_id(new_config['id_value'])[1],
                ).order_by('date')[0]
                bucket.available = (
                    bucket.available -
                    quote.value *
                    new_config['quantity']
                )
                new_configs.append(
                    InvestmentStockConfiguration(
                        stock_id=quote.stock_id,
                        quantity=new_config['quantity'],
                        bucket=bucket,
                        start=datetime.now()
                    )
                )
            InvestmentStockConfiguration.objects.bulk_create(new_configs)
            bucket.save()

        return EditConfiguration(bucket=bucket)


# pylint: disable=no-init
class Query(AbstractType):
    """
    We don't want to have any root queries here
    """
    invest_bucket = Field(GInvestmentBucket, args={'id': Argument(ID)})

    @staticmethod
    def resolve_invest_bucket(_self, args, context, _info):
        """
        The viewer represents the current logged in user
        """
        if not context.user.is_authenticated():
            return None

        return InvestmentBucket.objects.filter(
            Q(public=True) | Q(owner=context.user.profile)).get(
                id=from_global_id(args['id'])[1])

# pylint: enable=too-few-public-methods
# pylint: enable=no-init
