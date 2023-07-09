from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging

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

    def get_category(self):
        cates = []
        cates_soup = self.page_soup.select_one(self.selector["cate"])

        for cate_soup in cates_soup.find_all("li", recursive=False):
            text = cate_soup.select_one("a").get_text().strip()
            link = cate_soup.select_one("a").get("href").strip()
            cates.append([text, self.page_link + link])
        return cates

    def get_new(self, link):
        news = []
        cate_page_soup = BeautifulSoup(get_content(link), features="lxml")

        for new_link_soup in cate_page_soup.find_all("a"):
            link = new_link_soup.get("href")
            if link and link.startswith("/"):
                news.append(self.page_link + link)

        return list(set(news))

    def get_new_detail(self, link):
        new_page_soup = BeautifulSoup(get_content(link), features="lxml")
        title = new_page_soup.select_one(self.selector["newtitle"]).get_text().strip()
        time = new_page_soup.select_one(self.selector["newtime"]).get_text().strip()
        content = "   ".join(
            [
                p.get_text()
                for p in new_page_soup.select_one(self.selector["newcontent"]).find_all(
                    "p"
                )
            ]
        )
        return {"title": title, "time": time, "content": content}


    def process(self, num_of_cate=-1, num_of_new_per_cate=-1):
        count_cate=0
        cates = self.get_category()

        for cate in cates:
            count_new=0
            if count_cate == num_of_cate: 
                break
            try:
                news_link = self.get_new(cate[1])
            except AttributeError:
                logger.info("Skip cate: " + cate[1])
            else:
                count_cate+=1
                for new_link in news_link:
                    # continue of end
                    if count_new == num_of_new_per_cate: 
                        break
                    try:
                        new_data = self.get_new_detail(new_link)
                    except AttributeError:
                        logger.info("Skip news: " + new_link)
                    else:
                        count_new+=1
                        new_data["cate"] = cate[0]
                        self.news_data.append(new_data)


    def get(self):
        return self.news_data
