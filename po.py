from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from util import Util

class SearchResultValidation_PageObject(Util):
    URL = "https://www.github.com";
    DEFAULT_WAIT_TIME_IN_SECONDS = 5

    NEXT_PAGE = (By.XPATH, ".//a[@class='next_page']")
    SEARCH_FIELD = (By.XPATH, './/input[@data-test-selector="nav-search-input"]')
    RESULT_LIST = (By.XPATH, ".//ul[@class='repo-list']")
    NO_RESULTS = (By.XPATH, ".//div[@class='blankslate']")
    RESULT_ITEM = (By.XPATH, ".//li[contains(@class, 'repo-list-item')]")
    
    CURRENT_PAGE = ".//em[@class='current' and text()='{}']"
    RESULT_ITEM_TITLE = ".//li[contains(@class, 'repo-list-item')][{}]//div[@class='f4 text-normal']"
    RESULT_ITEM_DESC = ".//li[contains(@class, 'repo-list-item')][{}]//p[@class='mb-1']"
    RESULT_ITEM_LANGUAGE = ".//li[contains(@class, 'repo-list-item')][{}]//span[@itemprop='programmingLanguage']"
    RESULT_ITEM_UPDATED = ".//li[contains(@class, 'repo-list-item')][{}]//relative-time"
    RESULT_ITEM_LICENSE = ".//li[contains(@class, 'repo-list-item')][{}]//div[contains(text(), 'license')]"
    RESULT_ITEM_TAGS = ".//li[contains(@class, 'repo-list-item')][{}]//a[contains(@class, 'topic-tag')]"
    RESULT_ITEM_STARS = ".//li[contains(@class, 'repo-list-item')]{}]//a[contains(@href, 'stargazers')]"

    _driver: webdriver; 
    _actions: ActionChains;

    def check_init(self):
        return self._driver is not None

    def __init__(self, browser) -> None:
        self._driver = self.load_driver(browser=browser)
        self._actions = ActionChains(self._driver)

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
            return False
        except:
            return True
    
    def get_each_result_from_page(self):
        return WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_all_elements_located(self.RESULT_ITEM))

    def _get_detail(self, index, locator):
        """ Scraps the text from the required fields for the result at an index. If the field is not avaiable, None is returned
        """
        try:    
            element = self._driver.find_element(*(By.XPATH, locator.format(index)))
            self._driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.text
        except:
            return None

    def get_data(self, index):
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

    def next_page(self, current_page):
        """ Navigates to the next page and waits for the navigation to complete by checking the current page index.
        Returns:
            bool: true if navigation was done, false otherwise.
        """
        try:
            element = self._driver.find_element(*self.NEXT_PAGE)
            self._driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            WebDriverWait(self._driver, self.DEFAULT_WAIT_TIME_IN_SECONDS).until(EC.presence_of_all_elements_located((By.XPATH, self.CURRENT_PAGE.format(current_page + 1))))
            return True
        except:
            return False

