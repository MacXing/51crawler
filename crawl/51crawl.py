# -*- coding: utf-8 -*- 
# @Time : 2018/11/21 16:49 
# @Author : Allen 
# @Site :  爬取51job

from selenium import webdriver
from bs4 import BeautifulSoup
import os
from db.model_mongo import Mongodb
from log.log import Log


class Crawl51job:
    def __init__(self, browser_type='chrome', headless=False):
        self.driver = self.get_driver(browser_type, headless)
        self.url_list = []
        self.logger = Log().get_logger()
        self.mongodb = Mongodb()

    def get_driver(self, browser_type, headless):
        try:
            if browser_type == 'chrome':
                option = webdriver.ChromeOptions()
                if headless:
                    option.add_argument("-headless")
                    option.add_argument("--disable - gpu")
                return webdriver.Chrome(chrome_options=option)
            elif browser_type == 'firefox':
                option = webdriver.FirefoxOptions()
                if headless:
                    option.add_argument("-headless")
                    option.add_argument("--disable - gpu")
                return webdriver.Firefox(firefox_options=option)
            else:
                print("目前不支持{}浏览器".format(browser_type))
        except Exception as e:
            self.logger.error(e)

    def get_url(self, url):
        try:
            if not self.driver.current_url == url:
                self.driver.get(url)
        except:
            self.logger.error("Driver get {} error".format(url))

    def get_page_source(self):
        return self.driver.page_source

    def close_driver(self):
        self.driver.quit()

    def get_home_page(self, keyword):
        url = r'https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        self.get_url(url)
        self.find_keyword().send_keys(keyword)
        self.find_search_button().click()

    def get_next_page(self):
        try:
            self.driver.find_element_by_link_text("下一页").click()
            return True
        except:
            return False

    def crawl_keyword_url_detail(self, url):
        self.get_url(url)
        self.driver.implicitly_wait(3)
        document_dict = self.parser_keyword_url_detail(self.get_page_source(), url)
        self.mongodb.insert_document(document_dict)

    def parser_keyword_url_detail(self, html, url):
        try:
            info_dict = {}
            bs = BeautifulSoup(html, 'html.parser')
            div = bs.find('div', class_=['tHeader', 'tHjob'])
            info_dict['position_name'] = div.find('h1').text.strip()
            info_dict['salary'] = div.find('strong').text.strip()
            info_dict['company_name'] = div.find('p', 'cname').a['title'].strip()
            info_dict['company_href'] = div.find('p', 'cname').a['href'].strip()
            info_dict['welfare'] = div.find('p', class_=['msg', 'ltype'])['title'].strip()
            main_divs = bs.find('div', 'tCompany_main').find_all('div', 'tBorderTop_box')
            info_dict['position_info'] = main_divs[0].div.text.strip()
            info_dict['company_address'] = main_divs[1].div.text.strip()
            info_dict['company_info'] = main_divs[2].div.text.strip()
            info_dict['url'] = url
            return info_dict
        except Exception as e:
            self.logger.error("Error url:{} \n Error exception {}".format(url, e))

    def search_keyword(self, keyword):
        self.get_url_list(keyword)
        assert self.url_list, print('Crawl {} urls error'.format(keyword))
        print('Success crawl {} urls'.format(keyword))
        list(map(self.crawl_keyword_url_detail, self.url_list))
        print("Finished insert {} in Mongodb".format(keyword))

    def get_url_list(self, keyword):
        if not os.path.exists(os.path.join(os.getcwd(), '({})_urls.txt'.format(keyword))):
            self.get_home_page(keyword)
            while True:
                urls = self.parser_html(self.get_page_source())
                self.url_list += urls
                if not self.get_next_page():
                    break
            self.save_url(keyword)
        else:
            self.url_list = self.read_url_list(keyword)

    def save_url(self, keyword):
        with open('({})_urls.txt'.format(keyword), 'w', encoding='utf-8')as file:
            ([file.write(u + '\n') for u in self.url_list])

    def read_url_list(self, keyword):
        with open('({})_urls.txt'.format(keyword), 'r', encoding='utf-8') as file:
            url_list = [url.strip() for url in file.readlines()]
        return url_list

    def find_keyword(self):
        return self.driver.find_element_by_name('keyword')

    def find_search_button(self):
        return self.driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button')

    def parser_html(self, html):
        url_list = list()
        bs = BeautifulSoup(html, 'html.parser')
        for div in bs.find('div', 'dw_table').find_all('div', 'el'):
            try:
                href = div.find('p').span.a['href']
                url_list.append(href)
            except:
                pass
        return url_list


def main():
    crawl = Crawl51job(browser_type='firefox', headless=True)
    crawl.search_keyword('NLP算法工程师')
    crawl.close_driver()


if __name__ == '__main__':
    main()
