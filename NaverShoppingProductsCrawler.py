from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import  urlparse
import time


class ProductCrawler :
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
            dates.append(product.find(class_="date").text[4:]) #등록일 분자열 제거

        return dates

    def getPrices(self, soup):
        nv_mid = []
        for product in soup :
            try :
                price_text = product.find(class_="num _price_reload").text
                price_text = str(price_text).replace(",", "")
            except AttributeError as e :
                price_text = "판매 중지"
                print(e)
                nv_mid.append(price_text)
                continue

            nv_mid.append(price_text)

        return nv_mid

    def getProductImgsUrl(self, soup):
        imgs = []
        for product in soup :
            imgs.append(product.find(class_="_productLazyImg")['data-original'])

        return imgs


    def setProductSort(self):
        self.driver.find_element_by_css_selector("#_sort_review").click() # 리뷰 많은순
        # self.driver.find_element_by_css_selector("#_sort_date").click() # 등록일순
        time.sleep(2)

    def goPage(self, pageindex):
        # self.driver.execute_script("shop.detail.ReviewHandler.page(" + str(i) + ", '_review_paging');")
        self.driver.execute_script("shop.search.loader.goPage(" + str(pageindex) + ", '_result_paging');")
        time.sleep(2) # 이미지 로딩 대기

    def getUrlParsed(self, URL):
        url = urlparse(URL)
        return url.query.split("&")[0].split("=")[1]  # nvMid 값을 추출함


    def getContext(self, soup, pageIndex = None) :
        if pageIndex is None :
            pageIndex = 3

        nv_mids, names, prices, dates, img_urls = [], [], [], [], []

        for page in range(1, pageIndex+1):

            response = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(response, 'lxml')

            products = self.getProducts(soup) # get review divs

            nv_mids += self.getNv_mids(products)
            names += self.getProductNames(products)
            prices += self.getPrices(products)
            dates += self.getDates(products)
            img_urls += self.getProductImgsUrl(products)

            if page != pageIndex :
                self.goPage(page)


        return nv_mids, names, prices, dates, img_urls

    def getCrawlling(self, cat_id, pagecount = None):
        URL = "https://search.shopping.naver.com/search/category.nhn?cat_id=" + cat_id

        self.driver.get(URL)
        self.setProductSort() #리뷰 많은순 정렬
        time.sleep(2) #이미지 로딩 대기

        response = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(response, 'lxml')

        return self.getContext(soup, pagecount)

if __name__ == "__main__" :
    crawler = ProductCrawler()
    print(crawler.getCrawlling("50001203"))
    time.sleep(10)

