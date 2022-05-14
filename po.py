from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from util import Util

class SearchResultValidation_PageObject(Util):
    URL = "https://www.github.com";
    DEFAULT_WAIT_TIME_IN_SECONDS = 5

    NEXT_PAGE = (By.XPATH, ".//a[@class='next_page']")
    SEARCH_FIELD = (By.XPATH, './/input[@data-test-selector="nav-search-input"]')
    RESULT_LIST = (By.XPATH, ".//ul[@class='repo-list']")
    NO_RESULTS = (By.XPATH, ".//div[@class='blankslate']")
    RESULT_ITEM = (By.XPATH, ".//li[contains(@class, 'repo-list-item')]")
    RESULT_ITEM_TITLE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//div[@class='f4 text-normal']".format(i + 1))
    RESULT_ITEM_DESC = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//p[@class='mb-1']".format(i + 1))
    RESULT_ITEM_LANGUAGE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//span[@itemprop='programmingLanguage']".format(i + 1))
    RESULT_ITEM_UPDATED = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//relative-time".format(i + 1))
    RESULT_ITEM_LICENSE = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//div[contains(text(), 'license')]".format(i + 1))
    RESULT_ITEM_TAGS = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//a[contains(@class, 'topic-tag')]".format(i + 1))
    RESULT_ITEM_STARS = lambda i: (By.XPATH, ".//li[contains(@class, 'repo-list-item')]{}]//a[contains(@href, 'stargazers')]".format(i + 1))

    _driver: webdriver; 

    def check_init(self):
        return self._driver is not None

    def __init__(self, browser) -> None:
        self._driver = self.load_driver(browser=browser)

    def open_search(self):
        """ Opens the search page and waits for the search field to be visible
        """
        self._driver.get(self.URL)
        WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_element_located(self.SEARCH_FIELD))

    def search(self, query):
        """ Enters the search query into the search field and clicks on enter
        """
        search = self._driver.find_element(*self.SEARCH_FIELD)
        search.send_keys(query, Keys.ENTER)
        try: 
            # If the empty results placeholder is available, return an empty list. 
            # Else, results are available
            WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_all_elements_located(self.NO_RESULTS))
            print('No results found for query : {}'.format(query))
            return []
        except:
            pass 
        return WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_all_elements_located(self.RESULT_ITEM))

    def _get_detail(self, index, locator):
        """ Scraps the text from the required fields for the result at an index. If the field is not avaiable, None is returned
        """
        try:    
            print((By.XPATH, ".//li[contains(@class, 'repo-list-item')][{}]//div[@class='f4 text-normal']".format(index + 1)))
            return self._driver.find_element(*locator(index)).text
        except:
            return None

    def get_search_result_detail_from_page(self, index):
        """ Gets required result map for the result at an index
        """
        return {
            "title": self._get_detail(index, self.RESULT_ITEM_TITLE),
            "description":self._get_detail(index, self.RESULT_ITEM_DESC),
            "tags": self._get_detail(index, self.RESULT_ITEM_TAGS),
            "stars":self._get_detail(index, self.RESULT_ITEM_STARS),
            "language": self._get_detail(index, self.RESULT_ITEM_LANGUAGE),
            "licencedBy": self._get_detail(index, self.RESULT_ITEM_LICENSE),
            "updateTime": self._get_detail(index, self.RESULT_ITEM_UPDATED)
        }

    def next_page(self):
        """ Navigates to the next page.
        Returns:
            bool: true if navigation was done, false otherwise.
        """
        try:
            self._driver.click(*self.NEXT_PAGE)
            return True
        except:
            return False

