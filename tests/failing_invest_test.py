from selenium.webdriver.common.action_chains import ActionChains

# @mock_plaid_balance
# @mock_plaid_accounts
# @mock_plaid_transactions
# @pytest.mark.django_db(transaction=True)
# def test_invest_buy_bucket(selenium, live_server, client):
#     """
#     Test adding attr to bucket
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
#     selenium.find_element_by_id("save").click()
#     selenium.implicitly_wait(30)
#     bucket = user.profile.owned_bucket.get(name="IAMATESTBUCKET")
#     selenium.find_element_by_id("edit-comp").click()
#     selenium.implicitly_wait(30)
#     stock_field = selenium.find_element_by_class_name("MuiInput-inputSingleline-301")
#     stock_field.send_keys("Name1")
#     selenium.find_element_by_id("add-stock").click()
#     selenium.find_element_by_xpath("//button[contains(.,'Save')]").click()
#     selenium.implicitly_wait(30)
#     selenium.find_element_by_xpath("//button[contains(.,'Invest')]").click()
#     slider = selenium.find_element_by_class_name("rc-slider-handle")
#     actions = ActionChains(selenium)
#     # actions.drag_and_drop_by_offset(slider, 30, 0)
#     # actions.perform()
#     slider = selenium.find_element_by_class_name("rc-resdfs-handle")

#     EXECUTOR.wait_until_finished()
#     live_server.thread.terminate()
#     live_server.thread.join()