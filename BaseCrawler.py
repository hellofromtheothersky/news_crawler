from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging
from newspaper import Article
import json

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_content(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) from None
    else:
        return r.content


class BaseCrawler(ABC):
    page_link = ""
    page_soup = ""
    selector = {}
    news_data = []


    def __init__(self, link, selector):
        self.page_soup = BeautifulSoup(get_content(link), features="lxml")
        self.page_link = link
        self.selector = selector

    def __init__(self, name):
        with open('selector.json', 'r') as rf:
            pages_info=json.load(rf)
        self.page_link = pages_info[name]['page_link']
        self.selector = pages_info[name]['selector']
        self.page_soup = BeautifulSoup(get_content(self.page_link), features="lxml")

    def get_soup_in_selector_area(self, link, soup, selector_name):
        soup1=soup.select_one(self.selector[selector_name])
        if soup1:
            soup=soup1
        else:
            if selector_name+"@"+link in self.selector.keys():
                soup=soup.select_one(self.selector[selector_name+"@"+link])
            else: 
                return None

        return soup


    def get_category(self):
        cates = []
        cates_soup=self.get_soup_in_selector_area(self.page_link, self.page_soup, 'cate')

        for cate_soup in cates_soup.find_all("li", recursive=False):
            text = cate_soup.select_one("a").get_text().strip()
            link = cate_soup.select_one("a").get("href").strip()
            cates.append([text, self.page_link + link])
        return cates

    def get_new_list(self, link):
        news = []
        cate_page_soup = BeautifulSoup(get_content(link), features="lxml")
        cate_page_soup=self.get_soup_in_selector_area(link, cate_page_soup, 'listnew')

        for new_link_soup in cate_page_soup.find_all("a"):
            link = new_link_soup.get("href")
            if link and link.startswith("/"):
                news.append(self.page_link + link)

        return list(set(news))


    def get_new_detail(self, link):
        new_page_soup = BeautifulSoup(get_content(link), features="lxml")
        title = self.get_soup_in_selector_area(link, new_page_soup, 'newtitle').get_text().strip()
        time = self.get_soup_in_selector_area(link, new_page_soup, 'newtime').get_text().strip()
        content = "   ".join(
            [
                p.get_text()
                for p in new_page_soup.select_one(self.selector["newcontent"]).find_all(
                    "p"
                )
            ]
        )
        return {"title": title, "time": time, "content": content}
    

    def get_new_detail_auto_parse(self, link):
        article = Article(link)
        article.download()
        article.parse()
        return {"title": article.title, "time": article.publish_date, "content": article.text}


    def process(self, num_of_cate=-1, num_of_new_per_cate=-1):
        auto_parse=0
        cate_skip=0
        
        count_cate=0
        cates = self.get_category()

        for cate in cates:
            count_new=0
            if count_cate == num_of_cate: 
                break
            try:
                news_link = self.get_new_list(cate[1])
            except :
                logger.info("Skip cate: " + cate[1])
                cate_skip+=1
            else:
                count_cate+=1
                for new_link in news_link:
                    # continue of end
                    if count_new == num_of_new_per_cate: 
                        break
                    try:
                        new_data = self.get_new_detail(new_link)
                    except AttributeError:
                        auto_parse+=1
                        new_data = self.get_new_detail_auto_parse(new_link)
                        # logger.debug("Skip news: " + new_link)
                    count_new+=1
                    new_data["cate"] = cate[0]
                    self.news_data.append(new_data)
        logger.info("num of skip cate: "+ str(cate_skip))
        logger.info("num of auto-parse new: "+ str(auto_parse))

    def get(self):
        return self.news_data
    