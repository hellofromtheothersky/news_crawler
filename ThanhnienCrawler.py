from BaseCrawler import BaseCrawler
import json
class ThanhnienCrawler(BaseCrawler):
    pass

if __name__ == "__main__":
    with open('selector.json', 'r') as rf:
        pages_info=json.load(rf)

    crawler=ThanhnienCrawler(pages_info['thanhnien']['page_link'], pages_info['thanhnien']['selector'])
    crawler.process(num_of_cate=2, num_of_new_per_cate=2)
    for new in crawler.news_data:
        print(new['cate'], new['title'])