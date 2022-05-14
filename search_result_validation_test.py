import json
from selenium import webdriver
from po import SearchResultValidation_PageObject
from selenium.webdriver.support import expected_conditions as EC

class SearchResultValidation(SearchResultValidation_PageObject): 
    def __init__(self, browser) -> None:
        super().__init__(browser=browser)


handler = SearchResultValidation(browser='firefox')
handler.open_search()
handler.search("Security")
