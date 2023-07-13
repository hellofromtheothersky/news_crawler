from BaseCrawler import BaseCrawler
class Kenh14Crawler(BaseCrawler):
    pass

if __name__ == "__main__":
    crawler=Kenh14Crawler('kenh14')
    crawler.process(num_of_cate=-1, num_of_new_per_cate=1)
    for new in crawler.news_data:
        print(new['cate'], '-', new['title'])