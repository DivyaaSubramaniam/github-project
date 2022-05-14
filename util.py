import json
from selenium import webdriver

class Util:
    DEFAULT_CONFIG_PATH = "config.json"
    
    _driver: webdriver

    def load_driver(self, browser, config = DEFAULT_CONFIG_PATH):
        try:
            with open(config) as f:
                driver_path = json.load(f)['driver'][browser]
                if (browser == "firefox"):
                    self._driver = webdriver.Firefox(executable_path=driver_path)
            return self._driver
        except _:
            return None

    def __del__(self):
        if (self._driver is not None):
            self._driver.quit()