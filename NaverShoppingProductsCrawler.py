from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import  urlparse
import time


class NaverShoppingProductCrawler :
    driver = None

    def __init__(self):

        self.driver = webdriver.Chrome("chromedriver")
        self.driver.implicitly_wait(1)

    def __del__(self):
        self.driver.close()

    def getProducts(self, soup):
        return soup.find_all(class_="_model_list _itemSection")

    def getNv_mid(self, soup):
        nv_mid = []
        for product in soup :
            nv_mid.append(product['data-nv-mid'])

        return nv_mid


    def setReviewSort(self): # 리뷰 정렬 기준을 날자순으로 변경
        self.driver.find_element_by_css_selector("#_sort_review").click() # 리뷰 많은순
        # self.driver.find_element_by_css_selector("#_sort_date").click() # 등록일순

    def getUrlParsed(self, URL):
        url = urlparse(URL)
        return url.query.split("&")[0].split("=")[1]  # nvMid 값을 추출함


    def getContext(self, soup) :

        self.setReviewSort() # 리뷰 정렬을 날자순으로 바꾼다

        products = self.getProducts(soup)
        self.getNv_mid(products)

        print("sort complete")

    def getCrawlling(self, URL):
        self.driver.get(URL)

        response = self.driver.page_source.encode('utf-8')

        soup = BeautifulSoup(response, 'lxml')

        self.getContext(soup)
        print("crowling complete")

if __name__ == "__main__" :
    crawler = NaverShoppingProductCrawler()
    crawler.getCrawlling("https://search.shopping.naver.com/search/category.nhn?cat_id=50001203")

