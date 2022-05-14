from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from util import Util

class SearchResultValidation_PageObject(Util):
    URL = "https://www.github.com";
    DEFAULT_WAIT_TIME_IN_SECONDS = 10

    SEARCH_FIELD = (By.XPATH, './/input[@data-test-selector="nav-search-input"]')
    RESULT_LIST = (By.XPATH, ".//ul[@class='repo-list']")
    RESULT_ITEM = (By.XPATH, ".//li[contains(@class, 'repo-list-item')]")
    RESULT_ITEM_TITLE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//div[@class='f4 text-normal']".format(i + 1))
    RESULT_ITEM_DESC = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//p[@class='mb-1']".format(i + 1))
    RESULT_ITEM_LANGUAGE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//span[@itemprop='programmingLanguage']".format(i + 1))
    RESULT_ITEM_UPDATED = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//relative-time".format(i + 1))
    RESULT_ITEM_LICENSE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//div[contains(text(), 'license')]".format(i + 1))
    RESULT_ITEM_TAGS = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//a[contains(@class, 'topic-tag')]".format(i + 1))
    RESULT_ITEM_TAGS = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][%d]//a[contains(@href, 'stargazers')]".format(i + 1))

    _driver: webdriver; 

    def __init__(self, browser) -> None:
        self._driver = self.load_driver(browser=browser)

    def open_search(self):
        self._driver.get(self.URL)
        WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_element_located(self.SEARCH_FIELD))

    def search(self, query):
        search = self._driver.find_element(*self.SEARCH_FIELD)
        search.send_keys(query, Keys.ENTER)
        WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_element_located(self.RESULT_LIST))

    def get_search_result_detail(self):
        pass

    def get_all_search_results_in_page(self):
        pass

    def next_page(self):
        pass

