"""
All selenium tests
"""
from unittest import mock
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from BuyBitcoin.urls import EXECUTOR
from authentication.plaid_wrapper import PlaidAPI
from plaid_test_decorators import mock_plaid_balance, \
    mock_plaid_accounts, mock_plaid_transactions
from stocks.models import Stock
import test_stocks_model as stock_test


def setup_module(module):
    """
    Mock out any externals
    """
    stock_test.setup_module(module)


def teardown_module(module):
    """
    Restore externals
    """
    stock_test.teardown_module(module)


@mock.patch.object(PlaidAPI, 'current_balance', mock.MagicMock(return_value=0.0))
@mock.patch.object(PlaidAPI, 'account_name', mock.MagicMock(return_value="Acc Name"))
@mock.patch.object(PlaidAPI, 'income', mock.MagicMock(return_value=0.0))
@mock.patch.object(PlaidAPI, 'expenditure', mock.MagicMock(return_value=0.0))
@mock.patch.object(PlaidAPI, 'historical_data', mock.MagicMock(return_value=None))
@pytest.mark.django_db(transaction=True)
def test_signup(selenium, live_server, client):
    """
    Tests the signup flow
    """
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    user.save()
    client.login(username='temporary', password='temporary')
    cookie = client.cookies['sessionid']
    selenium.get('%s%s' % (live_server, '/login'))
    selenium.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/',
    })
    selenium.get('%s%s' % (live_server, '/'))
    selenium.implicitly_wait(30)
    test = selenium.find_element_by_id('link-button')
    test.click()
    selenium.switch_to.frame(selenium.find_element_by_id("plaid-link-iframe-1"))
    chase = selenium.find_element_by_class_name("Logo--chase")
    chase.click()
    selenium.find_element_by_id("username").send_keys("user_good")
    selenium.find_element_by_id("password").send_keys("pass_good")
    selenium.find_element_by_id("password").submit()
    elem = selenium.find_element_by_xpath("//button[contains(.,'Continue')]")
    WebDriverWait(selenium, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continue')]"))
    )
    elem.click()
    selenium.switch_to.default_content()
    selenium.find_element_by_id("menu-appbar-button").click()
    WebDriverWait(selenium, 120).until(
        EC.presence_of_element_located((By.ID, "logout"))
    )
    assert selenium.current_url == '%s%s' % (live_server, '/home')


@mock_plaid_balance
@mock_plaid_accounts
@mock_plaid_transactions
@pytest.mark.django_db(transaction=True)
def test_add_bucket(selenium, live_server, client):
    """
    Tests adding a bucket
    """
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    user.save()
    user.userbank.create(
        item_id='dummy1', access_token='dummy2',
        institution_name='dummy3', current_balance_field=0,
        account_name_field="dummy4", income_field=0,
        expenditure_field=0
    )
    client.login(username='temporary', password='temporary')
    assert user.profile.owned_bucket.count() == 0
    cookie = client.cookies['sessionid']
    selenium.get('%s%s' % (live_server, '/login'))
    selenium.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/',
    })
    selenium.get('%s%s' % (live_server, '/home'))
    selenium.implicitly_wait(30)
    newbuck = selenium.find_element_by_xpath("//button[contains(.,'New')]")
    newbuck.click()
    cancel = selenium.find_element_by_id("cancel")
    cancel.click()
    newbuck = selenium.find_element_by_xpath("//button[contains(.,'New')]")
    newbuck.click()
    buckname = selenium.find_element_by_id("name")
    buckname.send_keys("IAMATESTBUCKET")
    invest = selenium.find_element_by_id("investment")
    invest.send_keys("5000")
    save = selenium.find_element_by_id("save")
    save.click()
    assert user.profile.owned_bucket.count() == 1


# @mock_plaid_balance
# @mock_plaid_accounts
# @mock_plaid_transactions
# @pytest.mark.django_db(transaction=True)
# def test_delete_bucket(selenium, live_server, client):
#     """
#     Tests deleting a bucket
#     """
#     user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
#     user.save()
#     user.userbank.create(
#         item_id='dummy1', access_token='dummy2',
#         institution_name='dummy3', current_balance_field=0,
#         account_name_field="dummy4", income_field=0,
#         expenditure_field=0
#     )
#     client.login(username='temporary', password='temporary')
#     assert user.profile.owned_bucket.count() == 0
#     cookie = client.cookies['sessionid']
#     buck = InvestmentBucket.create_new_bucket(name="IAMATESTBUCKET", public=True, owner=user.profile)
#     assert user.profile.owned_bucket.count() == 1
#     selenium.get('%s%s' % (live_server, '/login'))
#     selenium.add_cookie({
#         'name': 'sessionid',
#         'value': cookie.value,
#         'secure': False,
#         'path': '/',
#     })
#     selenium.get('%s%s' % (live_server, '/home'))
#     delete_button = selenium.find_element_by_id("delete")
#     delete_button.click()
#     cancel_delete = selenium.find_element_by_id("keep")
#     cancel_delete.click()
#     assert user.profile.owned_bucket.count() == 0
#     delete_button.click()
#     selenium.implicitly_wait(30)
#     confirm_delete = selenium.find_element_by_id("delete2")
#     confirm_delete.click()
#     assert user.profile.owned_bucket.count() == 0


@mock_plaid_balance
@mock_plaid_accounts
@mock_plaid_transactions
@pytest.mark.django_db(transaction=True)
def test_add_attr_to_bucket(selenium, live_server, client):
    """
    Test adding attr to bucket
    """
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    user.save()
    user.userbank.create(
        item_id='dummy1', access_token='dummy2',
        institution_name='dummy3', current_balance_field=0,
        account_name_field="dummy4", income_field=0,
        expenditure_field=0
    )
    client.login(username='temporary', password='temporary')
    cookie = client.cookies['sessionid']
    selenium.get('%s%s' % (live_server, '/login'))
    selenium.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/',
    })
    selenium.get('%s%s' % (live_server, '/home'))
    selenium.implicitly_wait(30)
    newbuck = selenium.find_element_by_xpath("//button[contains(.,'New')]")
    newbuck.click()
    selenium.implicitly_wait(30)
    buckname = selenium.find_element_by_id("name")
    buckname.send_keys("IAMATESTBUCKET")
    invest = selenium.find_element_by_id("investment")
    invest.send_keys("5")
    save = selenium.find_element_by_id("save")
    save.click()
    selenium.implicitly_wait(30)
    add_attr = selenium.find_element_by_id("launch-edit")
    add_attr.click()
    selenium.implicitly_wait(30)
    attr_field = selenium.find_element_by_id("name")
    attr_field.send_keys("poooooop")
    attr_field.send_keys(Keys.RETURN)
    bucket = user.profile.owned_bucket.get(name="IAMATESTBUCKET")
    assert bucket.description.get(text="poooooop").text == "poooooop"


# @mock_plaid_balance
# @mock_plaid_accounts
# @mock_plaid_transactions
# @pytest.mark.django_db(transaction=True)
# def test_bucket_add_stock(selenium, live_server, client):
#     """
#     Test adding stock to bucket
#     """
#     user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
#     user.save()
#     user.userbank.create(
#         item_id='dummy1', access_token='dummy2',
#         institution_name='dummy3', current_balance_field=0,
#         account_name_field="dummy4", income_field=0,
#         expenditure_field=0
#     )
#     stock = Stock(
#         name="Name1", ticker="poooooop"
#     )
#     stock.save()
#     stock.daily_quote.create(
#         value=10000, date="2016-03-03"
#     )
#     client.login(username='temporary', password='temporary')
#     cookie = client.cookies['sessionid']
#     selenium.get('%s%s' % (live_server, '/login'))
#     selenium.add_cookie({
#         'name': 'sessionid',
#         'value': cookie.value,
#         'secure': False,
#         'path': '/',
#     })
#     selenium.get('%s%s' % (live_server, '/home'))
#     selenium.implicitly_wait(30)
#     newbuck = selenium.find_element_by_xpath("//button[contains(.,'New')]")
#     newbuck.click()
#     selenium.implicitly_wait(30)
#     buckname = selenium.find_element_by_id("name")
#     buckname.send_keys("IAMATESTBUCKET")
#     invest = selenium.find_element_by_id("investment")
#     invest.send_keys("5000")
#     save = selenium.find_element_by_id("save")
#     save.click()
#     selenium.implicitly_wait(30)
#     bucket = user.profile.owned_bucket.get(name="IAMATESTBUCKET")
#     assert bucket.get_stock_configs().count() == 0
#     edit_button = selenium.find_element_by_id("edit-comp")
#     edit_button.click()
#     selenium.implicitly_wait(30)
#     stock_field = selenium.find_element_by_id("stockname")
#     stock_field.send_keys("Name1")
#     add_stock = selenium.find_element_by_id("add-stock")
#     add_stock.click()
#     save_composition = selenium.find_element_by_xpath("//button[contains(.,'Save')]")
#     save_composition.click()
#     selenium.implicitly_wait(30)
#     assert bucket.get_stock_configs().count() == 1
