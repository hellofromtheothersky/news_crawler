from BaseCrawler import BaseCrawler
import json
class VtvCrawler(BaseCrawler):
    def get_category(self):
        source=BaseCrawler.get_category(self)
        source=[x for x in source if x[0]!='' and x[0]!='SỨC KHỎE']
        return source

if __name__ == "__main__":
    with open('selector.json', 'r') as rf:
        pages_info=json.load(rf)

    crawler=VtvCrawler(pages_info['vtv']['page_link'], pages_info['vtv']['selector'])
    crawler.process(num_of_cate=1, num_of_new_per_cate=0)
    news=crawler.get()
    for new in news:
        print(new['cate'], new['title'])