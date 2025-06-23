# base_login_test.py
import pytest
from selenium.common.exceptions import TimeoutException
from config import SeleniumConfig
class BaseLoginTest:
    @pytest.fixture
    def selenium(self):        
        config = SeleniumConfig(self.BASE_URL, disable_popups=True)
        config.setup_driver()
        yield config
        config.teardown_driver()

    def fill_login_form(self, selenium, email=None, password=None):
        if email:
            selenium.wait_and_send_keys(self.SELECTORS['email_input'], email)
        if password:
            selenium.wait_and_send_keys(self.SELECTORS['password_input'], password)
        selenium.wait_and_click(self.SELECTORS['submit_button'])
