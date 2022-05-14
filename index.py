import json
import sys
from po import SearchResultValidation_PageObject

class SearchResultValidation(SearchResultValidation_PageObject): 
    def __init__(self, browser) -> None:
        super().__init__(browser=browser)

def main(page_count, browser, output_json):
    data = {}
    handler = SearchResultValidation(browser=browser)
    if (not handler.check_init()):
        print("The driver was not initialized. Quitting") 
        exit(1)

    handler.open_search()
    results = handler.search("Security")
    
    if (results):
        for each in range(page_count):
            data.update({str(each + 1) : []})
            for index, _ in enumerate(handler.get_each_result_from_page()):
                data[str(each + 1)].append(handler.get_data(index + 1))
            if (not handler.next_page(each + 1)):
                break
    with open(output_json, "w+") as f:
        f.write(json.dumps(data, indent = 4))

if __name__ == "__main__":
    browser = 'firefox'
    output_json = "results.json"
    page_count = 2
    if (len(sys.argv) == 2):
        page_count = sys.argv[1]
    if (len(sys.argv) == 3):
        browser = sys.argv[2]
    elif (len(sys.argv) == 4):
        output_json = sys.argv[3]
    main(page_count=page_count, browser=browser, output_json=output_json)
