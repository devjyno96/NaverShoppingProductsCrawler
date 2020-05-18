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

    def getNv_mids(self, soup):
        nv_mid = []
        for product in soup :
            nv_mid.append(product['data-nv-mid'])

        return nv_mid

    def getProductNames(self, soup):
        names = []
        for product in soup :
            names.append(product.find(class_="link").text)

        return names


    def getDates(self, soup):
        dates = []
        for product in soup :
            dates.append(product.find(class_="date").text)

        return dates

    def getPrices(self, soup):
        nv_mid = []
        for product in soup :
            nv_mid.append(product.find(class_="num _price_reload").text)

        return nv_mid

    def getProductImgsUrl(self, soup):
        imgs = []
        for product in soup :
            imgs.append(product.find(class_="_productLazyImg")['src'])

        return imgs


    def setProductSort(self):
        self.driver.find_element_by_css_selector("#_sort_review").click() # 리뷰 많은순
        # self.driver.find_element_by_css_selector("#_sort_date").click() # 등록일순

    def goPage(self, pageindex):
        # self.driver.execute_script("shop.detail.ReviewHandler.page(" + str(i) + ", '_review_paging');")
        self.driver.execute_script("shop.search.loader.goPage(" + str(pageindex) + ", '_result_paging');")

    def getUrlParsed(self, URL):
        url = urlparse(URL)
        return url.query.split("&")[0].split("=")[1]  # nvMid 값을 추출함


    def getContext(self, soup) :
        products = self.getProducts(soup)
        self.getNv_mids(products)
        # self.goPage(2)
        print(self.getProductNames(products))
        print(self.getPrices(products))
        print(self.getDates(products))
        print(self.getProductImgsUrl(products))

    def getCrawlling(self, URL):
        self.driver.get(URL)
        self.setProductSort() #리뷰 많은순 정렬
        time.sleep(1) #이미지 로딩 대기

        response = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(response, 'lxml')

        self.getContext(soup)

if __name__ == "__main__" :
    crawler = NaverShoppingProductCrawler()
    crawler.getCrawlling("https://search.shopping.naver.com/search/category.nhn?cat_id=50001203")
    time.sleep(10)

