import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger()


class BrownAuthentication:
    @classmethod
    def authenticate(cls, driver: webdriver, username: str, password: str, duo_bypass: str):
        """Goes through Brown Auth process with provided username and password"""
        # Check if credentials are provided
        if not (username and password and duo_bypass):
            raise Exception(f"Credentials incorrectly configured!")

        logger.info('Logging in with Brown Authentication as {}...'.format(username))
        username_field = driver.find_element_by_xpath("//input[@id='username']")
        username_field.clear()
        username_field.send_keys(username)
        password_field = driver.find_element_by_xpath("//input[@id='password']")
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        logger.info('Successfully logged into Brown as {}'.format(username))
        time.sleep(2)  # wait a few seconds for Duo to load

        # Authenticate with DUO
        cls.__duo_authenticator(driver, duo_bypass)
        return

    @staticmethod
    def __duo_authenticator(driver: webdriver, duo_bypass: str):
        """Deals with the DUO Authenticator step of auth flow"""
        logger.info('Authenticating with Duo')
        iframes = driver.find_elements_by_tag_name("iframe")

        if len(iframes) > 0:
            # duo needs to be authenticated
            logger.info('Authenticating with Duo bypass code...')
            driver.switch_to.frame(iframes[0])
            duo_passcode_button = driver.find_element_by_xpath("//button[@id='passcode']")
            duo_passcode_button.click()
            passcode_field = driver.find_element_by_xpath("//input[@class='passcode-input']")
            passcode_field.clear()
            passcode_field.send_keys(duo_bypass)
            login_button = driver.find_element_by_xpath('//button[text()="Log In"]')
            login_button.click()
            logger.info('Successfully authenticated with Duo bypass code')
            time.sleep(2)

        return
