from BaseCrawler import BaseCrawler
class ThanhnienCrawler(BaseCrawler):
    pass

if __name__ == "__main__":
    crawler=ThanhnienCrawler('thanhnien')
    crawler.process(num_of_cate=-1, num_of_new_per_cate=1)
    for new in crawler.news_data:
        print(new['cate'], '-', new['title'])