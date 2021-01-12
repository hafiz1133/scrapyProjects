import scrapy
from scrapy.crawler import CrawlerProcess


class Eoddata(scrapy.Spider):
    name = 'eoddata'

    def start_requests(self):
        yield scrapy.Request(url='https://eoddata.com/symbols.aspx', callback=self.link)

    def link(self, response):
        for i in response.css('.p select#ctl00_cph1_cboExchange option'):
            nameStock = i.css('option::attr(value)').extract_first()
            yield scrapy.Request(url='https://eoddata.com/stocklist/' + nameStock + '.htm', callback=self.allLinks)

    def allLinks(self, response):
        fileticker = open('ticker.txt', 'a')
        filename = open('name.txt', 'a')
        for i in response.css('.ro'):
            data = i.css(' a::text').get()
            name = i.css(' td:nth-child(2)::text').get()
            fileticker.write(data + '\n')
            filename.write(name + '\n')
            print(data, name)
        for i in response.css('.re'):
            data1 = i.css(' a::text').get()
            name1 = i.css(' td:nth-child(2)::text').get()
            fileticker.write(data1 + '\n')
            filename.write(name1 + '\n')
            print(data1, name1)
        for i in response.css('.lett .ld'):
            link = i.css('a::attr(href)').extract_first()
            yield scrapy.Request(url='https://eoddata.com' + link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        
        fileticker = open('ticker.txt', 'a')
        filename = open('name.txt', 'a')
        for i in response.css('.ro'):
            data = i.css(' a::text').get()
            name = i.css(' td:nth-child(2)::text').get()
            fileticker.write(data + '\n')
            filename.write(name + '\n')
            print(data, name)
        for i in response.css('.re'):
            data1 = i.css(' a::text').get()
            name1 = i.css(' td:nth-child(2)::text').get()
            fileticker.write(data1 + '\n')
            filename.write(name1 + '\n')
            print(data1, name1)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Eoddata)
process.start()
