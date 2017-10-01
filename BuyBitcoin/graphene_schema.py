"""
The overarching GraphQL schema. Here is where all queries come together
to form one schema
"""
import graphene

import stocks.graphql
import trading.graphql
import authentication.graphql


# pylint: disable=too-few-public-methods
class Query(
        authentication.graphql.Query,
        stocks.graphql.Query,
        trading.graphql.Query,
        graphene.ObjectType):
    """
    Combination of all queries of all apps
    """
    pass


class Mutation(graphene.ObjectType):
    """
    List of all mutations we can perform
    """
    # pylint: disable=no-member
    add_trading_account = authentication.graphql.AddTradingAccount.Field()
    add_trade = trading.graphql.AddTrade.Field()
    add_stock = stocks.graphql.AddStock.Field()
    # pylint: enable=no-member
# pylint: enable=too-few-public-methods


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
