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
    # print(crawler.get_new_list('https://vtv.vn/the-thao.htm'))
    # print(crawler.get_new_list('https://vtv.vn/chinh-tri.htm'))
    # print(crawler.get_category())
    # print(crawler.get_new_detail('https://vtv.vn/chinh-tri/can-danh-gia-tinh-sau-sat-phu-hop-thuc-chat-cua-cong-tac-tiep-xuc-cu-tri-20230712103905343.htm'))
    crawler.process(num_of_cate=-1, num_of_new_per_cate=3)
    for new in crawler.news_data:
        print(new['cate'], new['title'])