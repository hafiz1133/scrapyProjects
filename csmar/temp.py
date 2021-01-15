import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv
from copy import deepcopy
import datetime
import string

csvheaders = ['name', 'phone number', 'office number', 'fax', 'email', 'link']
file = open('data123.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(file, fieldnames=csvheaders)
writer.writeheader()


class Spid(scrapy.Spider):
    name = 'sp'
    data = {'fulldetails': True, 'limit': 24, 'sortdirection': 'asc',
            'source': '@vroom-web/listing-1.3.7'}
    headers = {'Host': 'ims.vcrealtors.com', 'Connection': 'keep-alive', 'Content-Length': '343', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Origin': 'https://ims.vcrealtors.com', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'iframe', 'Referer': 'https://ims.vcrealtors.com/scripts/mgrqispi.dll?APPNAME=IMS&PRGNAME=IMSMemberLogin&ARGUMENTS=-AVCCA&SessionType=N&ServiceName=OSRH&NotLogin=Y', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'imssession=907766166; imslastConnect=1603909346324'}
    body = 'APPNAME=IMS&PRGNAME=IMSAgentsandOffices&ARGUMENTS=-A907766166%2C-N2%2CLastName%2C%28P%29+Agent+Nickname%2C%28P%29+Office+Name%2C%28P%29+City%2C%28P%29+Zip+Code&Member_Where_Category_Codes=%27AFF%27&Office_Where_Category_Codes=&Search_Type=A&LastName={}&%28P%29+Agent+Nickname=&%28P%29+Office+Name=&%28P%29+City=&%28P%29+Zip+Code=&List_Code_AFF='

    def start_requests(self):
        l = [v for v in string.ascii_lowercase]
        for i in l:
            yield scrapy.Request('https://ims.vcrealtors.com/scripts/mgrqispi.dll',
                                 body=self.body.format('{}'.format(i)), headers=self.headers, method='POST', meta={'letter': i})

    def parse(self, response):
        for link in [v for v in response.css('.table.table-striped tr a::attr(href)').extract() if 'Agent' in v]:
            yield scrapy.Request('https://ims.vcrealtors.com{}'.format(link), callback=self.parse_agent)
        if len([v for v in response.css('.table.table-striped tr a::attr(href)').extract() if 'Agent' in v]) < 100:
            letter = response.meta['letter']
            last = response.css('.table.table-striped tr a::text').extract()[-2][1]
            next_letter = chr(ord(last) + 1)
            yield scrapy.Request('https://ims.vcrealtors.com/scripts/mgrqispi.dll',
                                 body=self.body.format('{}{}'.format(letter, next_letter)), headers=self.headers, method='POST',
                                 meta={'letter': letter})

    def parse_agent(self, response):
        item = dict()
        item['link'] = response.url
        item['name'] = response.css('.memberName ::Text').extract_first('')
        for tr in response.css('.table.table-striped tr'):
            if 'Phone Number' in tr.css('td ::Text').extract()[0]:
                item['phone number'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
            if 'Office Phone' in tr.css('td ::Text').extract()[0]:
                item['office number'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
            if 'Fax' in tr.css('td ::Text').extract()[0]:
                item['fax'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
            if 'E-Mail' in tr.css('td ::Text').extract()[0]:
                item['email'] = ' '.join([v.strip() for v in tr.css('td ::Text').extract()[1:] if v.strip()])
        writer.writerow(item)
        file.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Spid)
process.start()
