from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import unittest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import warnings

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


class TestBoxProject(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.saucedemo.com/')

    def tearDown(self) -> None:
        self.driver.close()

    # TEST-1 LOGO DISPLAYED
    def test_logo_displayed(self):
        actual = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]')
        expected = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]')
        self.assertEqual(actual, expected, 'Logo is not displayed.')

    # TEST-2 NO USER AND PASSWORD
    def test_no_user_psw(self):
        self.driver.find_element(By.ID, 'login-button').click()
        assert 'Epic sadface: Username is required' in self.driver.page_source

    # TEST-3 USER AND PASSWORD WRONG
    def test_wrong_user_psw(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('username')
        self.driver.find_element(By.ID, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'login-button').click()
        assert 'Epic sadface: Username and password do not match any user in this service' in self.driver.page_source

    # TEST-4 LOGIN BUTTON DISPLAYED
    def test_login_displayed(self):
        login_button = self.driver.find_element(By.ID, 'login-button')
        self.assertIsNot(login_button, None)

    # TEST-5 RIGHT PAGE SHOP
    def test_shop_page(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        expected = 'https://www.saucedemo.com/inventory.html'
        actual = self.driver.current_url
        self.assertEqual(expected, actual, 'This is not the right page.')

    # TEST-6 FILTER WORKING
    def test_filter(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        dropdown = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div[2]/span/select')
        dd = Select(dropdown)
        dd.select_by_value('lohi')
        active_option_container = self.driver.find_element(By.XPATH,
                                                           '/html/body/div/div/div/div[1]/div[2]/div[2]/span/span')
        actual = active_option_container.get_attribute('innerText')
        self.assertEqual(actual, 'PRICE (LOW TO HIGH)')

    # TEST-7 CHEKOUT WORKING
    def test_checkout(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'add-to-cart-sauce-labs-onesie').click()
        self.driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
        self.driver.find_element(By.ID, 'checkout').click()
        actual = self.driver.get('https://www.saucedemo.com/cart.html')
        expected = 'https://www.saucedemo.com/checkout-step-one.html'
        self.assertNotEqual(actual, expected, 'Checkout not working')

    # TEST-8 LOGOUT WORKING
    def test_logout(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        self.driver.find_element(By.ID, 'logout_sidebar_link').click()
        actual = self.driver.get('https://www.saucedemo.com/inventory.html')
        expected = 'https://www.saucedemo.com/'
        self.assertNotEqual(actual, expected, 'logout failed')

    # TEST-9 USERNAME_2 IS INVALID
    def test_error_username2(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('locked_out_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[1]/div[1]/div/form/div[3]/h3')
        assert 'Epic sadface: Sorry, this user has been locked out.' in self.driver.page_source

    # TEST-10 USERNAME_3 IS WORKING
    def test_username3_working(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        assert 'Epic sadface: Username and password do not match any user in this service' not in self.driver.page_source

    # TEST-11 ADD AND REMOVE BUTTONS
    def test_add_and_remove(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack').click()
        self.driver.find_element(By.ID, 'remove-sauce-labs-backpack').click()
        try:
            self.driver.find_element(By.ID, 'remove-sauce-labs-backpack')
            assert False
        except NoSuchElementException:
            assert True

    # TEST-12 MENU BUTTON WORKING
    def test_menu_working(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        try:
            self.driver.find_element(By.ID, 'inventory_sidebar_link').click()
            assert True
        except ElementNotInteractableException:
            assert False

    # TEST-13 ABOUT PAGE
    def test_about_page(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        self.driver.find_element(By.ID, 'about_sidebar_link').click()
        actual = self.driver.current_url
        expected = 'https://saucelabs.com/'
        self.assertNotEqual(actual, expected, 'This is not the right page.')


if __name__ == '__main__':
    unittest.main()
