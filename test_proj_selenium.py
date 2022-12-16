import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import unittest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import warnings
import softest

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


class TestBoxProject(softest.TestCase):
    ERROR_MESSAGE = (By.XPATH, '//h3[@data-test="error"]')
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN = (By.NAME, 'login-button')
    DROPDOWN_FILTER = (By.CLASS_NAME, 'product_sort_container')
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, 'inventory_item_price')

    def setUp(self) -> None:
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.driver.get('https://www.saucedemo.com/')

    def tearDown(self) -> None:
        self.driver.quit()

    # TEST-1 LOGO DISPLAYED
    def test_logo_displayed(self):
        actual = self.driver.find_element(By.CLASS_NAME, 'login_logo')
        self.soft_assert(self.assertTrue, actual.is_displayed(), 'Logo is not displayed.')

    # TEST-2 NO USER AND PASSWORD
    def test_no_user_psw(self):
        login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'login-button')))
        login_button.click()
        actual_error = self.driver.find_element(*self.ERROR_MESSAGE).text
        expected_error = 'Epic sadface: Username is required'
        self.soft_assert(self.assertEqual,
                         actual_error, expected_error, f'expected: {expected_error} actual:{actual_error}')

    # TEST-3 USER AND PASSWORD WRONG
    def test_wrong_user_psw(self):
        self.driver.find_element(*self.USERNAME).send_keys('username')
        self.driver.find_element(*self.PASSWORD).send_keys('password')
        self.driver.find_element(*self.LOGIN).click()
        actual_error = self.driver.find_element(*self.ERROR_MESSAGE).text
        expected_error = 'Epic sadface: Username and password do not match any user in this service'
        self.soft_assert(self.assertEqual, actual_error, expected_error,
                         f'expected: {expected_error} actual: {actual_error}')

    # TEST-4 LOGIN BUTTON DISPLAYED
    def test_login_displayed(self):
        login_button = self.driver.find_element(By.ID, 'login-button')
        self.soft_assert(self.assertTrue, login_button.is_displayed(), 'Error Login Button is not displayed.')

    # TEST-5 RIGHT PAGE SHOP
    def test_shop_page(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        expected = 'https://www.saucedemo.com/inventory.html'
        actual = self.driver.current_url
        self.soft_assert(self.assertEqual, expected, actual, 'This is not the right page.')

    # TEST-6 FILTER WORKING
    def test_filter(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        dropdown = Select(self.driver.find_element(*self.DROPDOWN_FILTER))
        dropdown.select_by_visible_text('Price (low to high)')
        prices_list = self.driver.find_elements(*self.INVENTORY_ITEM_PRICE)
        sorted = True
        for i in range(len(prices_list) - 1):
            for j in range(i + 1, len(prices_list)):
                print(prices_list[i].text)
                # print(prices_list[j].text)
                if float(prices_list[i].text.replace('$', '')) > float(prices_list[j].text.replace('$', '')):
                    sorted = False
        self.soft_assert(self.assertTrue, sorted, 'List is not sorted.')

    # TEST-7 CHEKOUT WORKING
    def test_checkout(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'add-to-cart-sauce-labs-onesie').click()
        self.driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
        self.driver.find_element(By.ID, 'checkout').click()
        actual = self.driver.current_url
        expected = 'https://www.saucedemo.com/checkout-step-one.html'
        self.soft_assert(self.assertEqual, actual, expected, 'Checkout not working')

    # TEST-8 LOGOUT WORKING
    def test_logout(self):
        user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user-name')))
        user.send_keys('standard_user')
        password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password.send_keys('secret_sauce')
        login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login-button')))
        login.click()
        menu = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'react-burger-menu-btn')))
        menu.click()
        time.sleep(5)
        logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'logout_sidebar_link')))
        logout.click()
        actual = self.driver.current_url
        expected = 'https://www.saucedemo.com/'
        self.soft_assert(self.assertEqual, actual, expected, 'logout failed')

    # TEST-9 USERNAME_2 IS INVALID
    def test_error_username2(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('locked_out_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        actual_error = self.driver.find_element(*self.ERROR_MESSAGE).text
        expected_error = 'Epic sadface: Sorry, this user has been locked out.'
        self.soft_assert(self.assertEqual, actual_error == expected_error,
                         f'expected: {expected_error} actual: {actual_error}')

    # TEST-10 USERNAME_3 IS WORKING
    def test_username3_working(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        actual = self.driver.current_url
        expected = 'https://www.saucedemo.com/inventory.html'
        self.soft_assert(self.assertEqual, actual, expected, 'Problem user not working.')

    # TEST-11 ADD AND REMOVE BUTTONS
    def test_add_and_remove(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        add_to_cart = self.driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack')
        add_to_cart.click()
        self.driver.find_element(By.ID, 'remove-sauce-labs-backpack').click()
        self.soft_assert(self.assertEqual, add_to_cart.text, 'ADD TO CART',
                         'Error product is not removed from the shopping cart.')

    # TEST-12 MENU BUTTON WORKING
    def test_menu_working(self):
        username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user-name')))
        username.send_keys('standard_user')
        password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password.send_keys('secret_sauce')
        login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login-button')))
        login.click()
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        menu_item_list = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        self.soft_assert(self.assertEqual, len(menu_item_list), 4, 'Error menu list not loaded properly.')

    # TEST-13 ABOUT PAGE
    def test_about_page(self):
        self.driver.find_element(By.ID, 'user-name').send_keys('problem_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.NAME, 'login-button').click()
        self.driver.find_element(By.ID, 'react-burger-menu-btn').click()
        self.driver.find_element(By.ID, 'about_sidebar_link').click()
        actual = self.driver.current_url
        expected = 'https://saucelabs.com/'
        self.soft_assert(self.assertEqual, expected, actual, 'This is not the right page.')


if __name__ == '__main__':
    unittest.main()
