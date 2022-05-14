import json
from po import SearchResultValidation_PageObject

class SearchResultValidation(SearchResultValidation_PageObject): 
    def __init__(self, browser) -> None:
        super().__init__(browser=browser)

def main(results):
    data = {}
    handler = SearchResultValidation(browser='firefox')
    if (not handler.check_init()):
        print("The driver was not initialized. Quitting") 
        exit(1)

    handler.open_search()
    results = handler.search("Security")
    if (len(results)):
        for index, _ in enumerate(results):
            data.update({str(index + 1) : handler.get_search_result_detail_from_page(index)})
            if (not handler.next_page()): break
        with open(results, "w+") as f:
            f.write(json.dumps(data, indent = 4))

if __name__ == "__main__":
    main(results="results.json")

