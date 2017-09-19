"""
The overarching GraphQL schema. Here is where all queries come together
to form one schema
"""
import graphene

import stocks.graphene
import trading.graphene
import authentication.graphene


# pylint: disable=too-few-public-methods
class Query(
        authentication.graphene.Query,
        stocks.graphene.Query,
        trading.graphene.Query,
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
    add_trading_account = authentication.graphene.AddTradingAccount.Field()
    # pylint: enable=no-member
# pylint: enable=too-few-public-methods


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
