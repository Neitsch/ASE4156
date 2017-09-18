"""
GraphQL definitions for the Authentication App
"""
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene import AbstractType, Field, relay


# pylint: disable=too-few-public-methods
class GUser(DjangoObjectType):
    """
    GraphQL representation of a User
    """
    class Meta:
        """
        Meta Model for User. We must make sure to not expose
        the whole usere object
        """
        model = User
        only_fields = ('id', 'trading_accounts', 'username')
        interfaces = (relay.Node, )


# pylint: disable=no-init
class Query(AbstractType):
    """
    Query represents the entry method for a GraphQL request
    """
    viewer = Field(GUser, )

    @staticmethod
    def resolve_viewer(_, __, context, ____):
        """
        The viewer represents the current logged in user
        """
        if not context.user.is_authenticated():
            return None
        return context.user
# pylint: enable=too-few-public-methods
# pylint: enable=no-init
