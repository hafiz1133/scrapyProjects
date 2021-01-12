"""
This is Used to scrape description from youtube vedio.
"""
import scrapy
import datetime
import time
from scrapy.crawler import CrawlerProcess
import csv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from copy import deepcopy
from selenium.webdriver.firefox.options import Options as ff_options

csv_columns = ['url', 'description']
csvfile = open('youtubeData-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


class Youtube(scrapy.Spider):
    name = 'youtube'

    def start_requests(self):
        yield scrapy.Request(url='https://www.youtube.com/c/KiteHQ/videos')

    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)
        driver.maximize_window()
        time.sleep(5)
        previous_height = None
        height = 0
        while (True):
            previous_height = deepcopy(height)
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(5)
            if height == previous_height:
                break
        response1 = scrapy.Selector(text=driver.page_source)
        for i in response1.css('#details'):
            link = i.css('.yt-simple-endpoint.style-scope.ytd-grid-video-renderer::attr(href)').extract_first()
            url = 'https://www.youtube.com' + str(link)
            yield scrapy.Request(url=url, callback=self.finale)
        driver.close()

    def finale(self, response):
        """
        It opens a browser and get description and url also
        :param response:
        :return:
        """
        options = ff_options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(response.url)
        driver.maximize_window()
        time.sleep(5)
        response1 = scrapy.Selector(text=driver.page_source)
        item = dict()
        item['url'] = response.url
        item['description'] = ''.join(
            response1.css('.content.style-scope.ytd-video-secondary-info-renderer ::text').extract())
        writer.writerow(item)
        driver.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Youtube)
process.start()
