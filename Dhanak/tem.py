import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
import csv

class Dhanak(scrapy.Spider):
    name='dhanak'

    def start_requests(self):

        yield scrapy.Request(url='https://www.dhanak.com.pk/product-category/dupatta/',
                             callback=self.parse)
    def parse(self, response):
        for i in response.css('.product-small.box'):
            try:
                name=i.css('.name.product-title.woocommerce-loop-product__title a::text').extract_first()
                s=i.css('.title-wrapper a::attr(href)').extract_first()

                print("hy")

            except:
                pass



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Dhanak)
process.start()