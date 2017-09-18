from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene import AbstractType, Field, relay


class GUser(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'trading_accounts', 'username')
        interfaces = (relay.Node, )


class Query(AbstractType):
    viewer = Field(GUser, )

    @staticmethod
    def resolve_viewer(cls, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
