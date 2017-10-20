from django.test import LiveServerTestCase
from selenium.webdriver.support import ui
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import Client
from django.contrib.auth.models import User
from time import sleep



class ExampleTestCase(LiveServerTestCase):
    def setUp(self):
        #self.vdisplay = Display(visible=1, size=(1024, 768))
        #self.vdisplay.start()

        self.selenium = WebDriver()
        super().setUp()

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

        #self.vdisplay.stop()

    def test_example(self):
        self.client = Client()
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.user.save()
        self.client.login(username='temporary', password='temporary')
        cookie = self.client.cookies['sessionid']
        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.selenium.get('%s%s' % (self.live_server_url, '/home'))
        self.selenium.implicitly_wait(30)
        test = self.selenium.find_element_by_id('link-button')
        test.click()
        self.selenium.switch_to.frame(self.selenium.find_element_by_id("plaid-link-iframe-1"))
        chase = self.selenium.find_element_by_class_name("Logo--chase")
        chase.click()
        self.selenium.find_element_by_id("username").send_keys("user_good")
        self.selenium.find_element_by_id("password").send_keys("pass_good")
        self.selenium.find_element_by_id("password").submit()
        sleep(5)
        self.selenium.find_element_by_xpath("//button[contains(.,'Continue')]").click()
        self.selenium.switch_to.default_content()
        sleep(50)
