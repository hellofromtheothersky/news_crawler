from BaseCrawler import BaseCrawler
class VtvCrawler(BaseCrawler):
    pass

if __name__ == "__main__":
    crawler=VtvCrawler('vtv')
    crawler.process(num_of_cate=-1, num_of_new_per_cate=3)
    for new in crawler.news_data:
        print(new['cate'], new['title'])