from po import SearchResultValidation_PageObject

class SearchResultValidation(SearchResultValidation_PageObject): 
    def __init__(self, browser) -> None:
        super().__init__(browser=browser)


handler = SearchResultValidation(browser='firefox')
handler.open_search()
handler.search("Security")
