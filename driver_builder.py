import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException


class DriverBuilder:
    def __init__(self, headless_mode=False):
        self.headless_mode = headless_mode
        self.proxy = None

    def set_options(self):
        options = Options()
        options.headless = self.headless_mode
        options.add_argument("--lang=en")
        options.add_argument("log-level=3")
        return options

    def set_proxy(self, proxy):
        self.proxy = proxy

    def get_driver(self):
        options = self.set_options()
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        try:
            driver = webdriver.Chrome(
                options=options
            )

        except (SessionNotCreatedException, WebDriverException) as e:
            logging.info(e)
            driver = webdriver.Chrome(
                options=options
            )
        return driver
