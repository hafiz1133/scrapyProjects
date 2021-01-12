import json
import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
import csv
csv_columns = ['image', 'Name', 'price','Cut out Price','size','Product URL']
csvfile = open('dhanak-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()
class Dhanak(scrapy.Spider):
    name = 'dhanak'
    start_url = ['https://www.dhanak.com.pk/']

    def start_requests(self):

        yield scrapy.Request(url='https://www.dhanak.com.pk/',
                             callback=self.link)

    def link(self, response):
        for j in response.css('.flex-col.hide-for-medium.flex-left li a::attr(href)').extract()[2:]:
            if not 'https:' in j:
                j = 'https:'+j
            yield scrapy.Request(url=j,callback=self.parse)

            for k in range(1, 9): # This is used for pagination
                new = j+'page/'+str(k)
                yield scrapy.Request(url=new, callback=self.parse)

    def parse(self,response):
        item = dict()
        try:
            for i in response.css('.product-small.box'):
                name = i.css('.name.product-title.woocommerce-loop-product__title a::text').extract_first()
                image = i.css('.image-fade_in_back img::attr(src)').extract_first()
                size = i.css('.variable-item-span.variable-item-span-button::text').extract()
                prodUrl=i.css('.title-wrapper a::attr(href)').extract_first()
                cutout = i.css('.price del bdi::text').extract_first('')
                if cutout:
                    # cutout=cutout.strip()
                    item['Cut out Price']=cutout
                    price = i.css('.price bdi::text')[1].extract()
                    # price=price.strip()
                else:
                    price = i.css('bdi::text').get()
                    # price=price.strip()
                item['image'] = image
                item['Name'] = name
                item['price'] = price
                item['size'] = size
                item['Product URL']=prodUrl
                writer.writerow(item)
        except:
            pass

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(Dhanak)
process.start()