import scrapy
import datetime
import time
from scrapy.crawler import CrawlerProcess
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as ff_options



csv_columns = ['url','name','stars', 'review', 'price','total_guest', 'bedrooms', 'bed','bath']
csvfile = open('hotelData500-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()
class Airbnb(scrapy.Spider):
    name = 'sports'
    # start_urls=['https://www.airbnb.com/rooms/20386695?source_impression_id=p3_1607933241_6BIbEYFCnbqQzZLF&guests=1&adults=1']
    def start_requests(self):
        from random import randint
        for i in range(500):
            random_number = randint(11111111, 99999999)
            url='https://www.airbnb.com/rooms/'+str(random_number)
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):


            # options = ff_options()
        # options.add_argument('--headless')
        driver = webdriver.Firefox()
        driver.get(response.url)
        time.sleep(5)
        response1 = scrapy.Selector(text=driver.page_source)

        name=response1.css('._14i3z6h::text').extract_first()
        if name:
            item = dict()
            item['url'] = response.url
            item['name'] = name
            stars= response1.css('._1jpdmc0::text').extract_first()
            if stars is None:
                item['stars'] =""
            else:
                item['stars']=stars
            review= response1.css('._1sqnphj::text').extract_first()
            if review is None:
                item['review']=""
            else:
                item['review']=review.replace("(", "").replace(")", "")
            price=response1.css('._pgfqnw::text').extract_first()
            perDay=response1.css('._1l0ezq0::text').extract_first()
            item['price'] = price +" "+perDay
            item['total_guest'] = response1.css('._tqmy57').css('span::text')[0].extract()
            item['bedrooms'] = response1.css('._tqmy57').css('span::text')[2].extract()
            item['bed'] = response1.css('._tqmy57').css('span::text')[4].extract()
            item['bath'] = response1.css('._tqmy57').css('span::text')[6].extract()
            driver.close()
            writer.writerow(item)
        else:
            driver.quit()






process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Airbnb)
process.start()



