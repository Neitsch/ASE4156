"""
This file helps to test graphql queries and verify that the "big picture" works
"""
import pytest
from graphene.test import Client
from BuyBitcoin.graphene_schema import SCHEMA
from django.contrib.auth.models import User
from trading.models import TradingAccount, Trade
from stocks.models import Stock


def request_create(request):
    """
    Creates a fully functional environment that we can test on
    """
    request.user = User.objects.create(username='testuser2', password='pwd')
    account = TradingAccount(profile=request.user.profile, account_name="testAccount2")
    account.save()
    stock = Stock(name="Google", ticker="GOOGL")
    stock.save()
    trade = Trade(quantity=2, account=account, stock=stock)
    trade.save()

    request.user = User.objects.create(username='testuser1', password='pwd')
    account = TradingAccount(profile=request.user.profile, account_name="testAccount1")
    account.save()
    trade = Trade(quantity=1, account=account, stock=stock)
    trade.save()
    return request


@pytest.mark.django_db
# pylint: disable=invalid-name
def test_big_gql(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = request_create(rf.post('/graphql'))
    client = Client(SCHEMA)
    executed = client.execute("""
        {
            viewer {
                username
                profile {
                    tradingAccounts {
                        edges {
                            node {
                                accountName
                                trades {
                                    edges {
                                        node {
                                            quantity
                                            stock {
                                                ticker
                                                name
                                                trades {
                                                    edges {
                                                        node {
                                                            account {
                                                                accountName
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """, context_value=request)
    snapshot.assert_match(executed)
