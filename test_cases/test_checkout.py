import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.LoginPage import LoginPage
from pages.AllItems import AllItems
from pages.Cart import Cart
from pages.ExpandedList import ExpandedList
from configurations.config import LOGIN_URL, VALID_USERNAME, VALID_PASSWORD

class TestCheckout:
    valid_username = 'standard_user'
    valid_password = 'secret_sauce'

    # @pytest.mark.smoke
    @allure.feature('Checkout')
    @allure.story('Successful order')
    def test_verify_successful_order(self, driver, login):
        expected_confirmation_element = (By.XPATH, "//h2[text()='Thank you for your order!']")

        all_items = AllItems(driver)
        all_items.verify_cart_is_empty()
        all_items.add_product_to_cart_by_name("Sauce Labs Bike Light")
        all_items.open_cart()

        cart = Cart(driver)
        cart.checkout_from_cart_view()
        cart.enter_checkout_credentials_and_continue()
        cart.finish_checkout()

        cart.assert_element_visible(*expected_confirmation_element)

    # @pytest.mark.smoke
    @allure.feature('Checkout')
    @allure.story('Cancel order')
    def test_verify_cancel_order(self, driver):
        expected_element_after_cancel = (By.XPATH, "//span[@class='title']")

        login_page = LoginPage(driver)
        login_page.open_login_page(LOGIN_URL)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        all_items = AllItems(driver)
        all_items.verify_cart_is_empty()
        all_items.add_product_to_cart_by_name("Sauce Labs Onesie")
        all_items.open_cart()

        cart = Cart(driver)
        cart.checkout_from_cart_view()
        cart.enter_checkout_credentials_and_continue()
        cart.cancel_checkout()

        cart.assert_element_visible(*expected_element_after_cancel)
