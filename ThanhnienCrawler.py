from BaseCrawler import BaseCrawler
import json
class ThanhnienCrawler(BaseCrawler):
    pass

if __name__ == "__main__":
    with open('selector.json', 'r') as rf:
        pages_info=json.load(rf)

    crawler=ThanhnienCrawler(pages_info['thanhnien']['page_link'], pages_info['thanhnien']['selector'])
    crawler.process(num_of_cate=-1, num_of_new_per_cate=1)
    for new in crawler.news_data:
        print(new['cate'], '-', new['title'])
    # crawler.get_new_detail_v2('https://thanhnien.vn/xet-xu-dai-an-chuyen-bay-giai-cuu-muon-to-chuc-chuyen-bay-phai-chi-tien-hoi-lo-185230711234045462.htm')