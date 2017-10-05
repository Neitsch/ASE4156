"""
This file helps to test graphql queries and verify that the "big picture" works
"""
import string
import random
import pytest
from graphene.test import Client
from BuyBitcoin.graphene_schema import SCHEMA
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from trading.models import TradingAccount, Trade
from stocks.models import Stock
from stocks.historical import create_stock


def request_create(request):
    """
    Creates a fully functional environment that we can test on
    """
    post_save.disconnect(receiver=create_stock, sender=Stock)
    stock = Stock(name="Google", ticker="GOOGL")
    stock.save()

    pw2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    user2 = User.objects.create(username='testuser2', password=pw2)
    account2 = TradingAccount(profile=user2.profile, account_name="testAccount2")
    account2.save()
    trade2 = Trade(quantity=2, account=account2, stock=stock)
    trade2.save()

    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    account1 = TradingAccount(profile=request.user.profile, account_name="testAccount1")
    account1.save()
    trade1 = Trade(quantity=1, account=account1, stock=stock)
    trade1.save()
    return request


@pytest.mark.django_db
# pylint: disable=invalid-name
def test_mutation_add_trading_account(rf, snapshot):
    """
    This submits a massive graphql query to verify all fields work
    """
    # pylint: enable=invalid-name
    request = rf.post('/graphql')
    pw1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    request.user = User.objects.create(username='testuser1', password=pw1)
    client = Client(SCHEMA)
    acc_name = "Test 1"
    executed = client.execute("""
        mutation {{
          addTradingAccount(name: "{}") {{
            account {{
              accountName
            }}
          }}
        }}
    """.format(acc_name), context_value=request)
    snapshot.assert_match(executed)
    acc = TradingAccount.objects.get(profile__user__id=request.user.id)
    ex_acc = executed['data']['addTradingAccount']['account']['accountName']
    assert ex_acc == acc.account_name


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
