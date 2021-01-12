import re
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from urllib.parse import urlparse
import mysql.connector
import json
from copy import deepcopy
import datetime
import csv

API_KEY = 'cddda3d4f906978072875aeba9e8d1c8'  ## Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup

csv_columns = ['name', 'email', 'phone', 'phone2', 'company', 'city', 'country', 'link', 'designation',
               'industry']
csvfile = open('csv_files.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def create_google_url(query, site=''):
    google_dict = {'q': query, 'num': 100, }
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
        return 'https://www.google.com/search?' + urlencode(google_dict)
    return 'https://www.google.com/search?' + urlencode(google_dict)


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {'CLOSESPIDER_PAGECOUNT': 100000, 'ROBOTSTXT_OBEY': False, 'DOWNLOAD_TIMEOUT': 1000,
                       'CONCURRENT_REQUESTS': 20, 'AUTOTHROTTLE_ENABLED': False,
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
                       'RETRY_TIMES': 5, 'RETRY_HTTP_CODES': [302]}
    proxy = 'http://7c53d2a440d14295a005d02ea0d0a724:@proxy.crawlera.com:8010/'
    DOWNLOAD_TIMEOUT = 1000
    CONCURRENT_REQUESTS = 200
    CONCURRENT_REQUESTS_PER_DOMAIN = 200
    RETRY_TIMES = 5
    RETRY_HTTP_CODES = ['302']
    AUTOTHROTTLE_ENABLED = False
    cities = []
    designations = []
    industries = []
    handle_httpstatus_list = [429]
    current_index = 0
    url_template = 'http://api.scraperapi.com?api_key=cddda3d4f906978072875aeba9e8d1c8&url={}'
    connection = None
    cursor = None
    count = 0
    csv_count = 0


    def get_connection(self):
        self.connection = mysql.connector.connect(host='104.155.184.16',
                                                  database='scraping',
                                                  user='root',
                                                  password='Password123$')
        self.cursor = self.connection.cursor()

    def get_cities(self):
        file_ = open('cities.csv', 'r', encoding='ISO-8859-1')
        city_rows = file_.read()
        city_rows = city_rows.split('\n')
        cities = []
        for city_row in city_rows:
            city_row = city_row.split(',')
            cities.append(city_row)
        return cities

    def get_designations(self):
        file_ = open('designations.csv', 'r', encoding='ISO-8859-1')
        designation_rows = file_.read()
        designation_rows = designation_rows.split('\n')
        designations = []
        for designation_row in designation_rows:
            designation_row = designation_row.split(',')
            if len(designation_row) > 1:
                designations.append(designation_row[1])
        return designations

    def get_industries(self):
        file_ = open('designations.csv', 'r', encoding='ISO-8859-1')
        designation_rows = file_.read()
        designation_rows = designation_rows.split('\n')
        designations = []
        for designation_row in designation_rows:
            designation_row = designation_row.split(',')
            designations.append(designation_row[0])
        return designations

    def start_requests(self):
        self.get_connection()
        self.cities = self.get_cities()
        self.designations = self.get_designations()
        self.industries = self.get_industries()
        for city in self.cities:
            if len(city) > 1 :
                for designation in self.designations:
                    for industry in self.industries:
                        designation = designation.split('and')[0]
                        designation = designation.split('And')[0]
                        # query = 'site:http://linkedin.com/in/ intitle:"{designation}" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "{city}" AND "{industry}"'.format('ceo', '{}, {}'.format('london', 'united kingdom'))
                        # query = 'site:http://linkedin.com/in/ intitle:"ceo" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "london" AND ("information technology" OR "software")'
                        query = 'site:http://linkedin.com/in/ intitle:"{}" intext:("gmail.com" OR "yahoo.com" OR "hotmail.com")  AND "{}" AND "{}"'.format(
                            designation, city, industry)
                        url = create_google_url(query)
                        yield scrapy.Request(url, callback=self.parse, meta={'pos': 0, 'city': city,
                                                                                      'url': url, 'start': 100,
                                                                                      'industry': industry,
                                                                                      'designation': designation,
                                                                                      'proxy': self.proxy})

    def parse(self, response):
        items = []
        industry = response.meta['industry']
        designation = response.meta['designation']
        start = deepcopy(response.meta['start'])
        city = response.meta['city']
        print(response.status)
        print(response.meta['url'])
        if response.status == 429:
            yield scrapy.Request(response.url, callback=self.parse, meta={'pos': 0, 'city': city,
                                                                          'url': response.meta['url'], 'start': start,
                                                                          'industry': industry,
                                                                          'designation': designation,
                                                                          'proxy': self.proxy},
                                 dont_filter=True)
            return
        values_str = ''
        if len(response.css('.rc')) > 99:
            url = '{}&start={}'.format(response.meta['url'], response.meta['start'])
            yield scrapy.Request(url, callback=self.parse,
                                 meta={'pos': 0, 'city': city, 'url': response.meta['url'], 'start': start + 100,
                                       'industry': industry, 'designation': designation, 'proxy': self.proxy},
                                 dont_filter=True)
        for result in response.css('.rc'):
            item = dict()
            item['city'] = city[0].replace('"', '')
            item['country'] = city[1].replace('"', '')
            item['link'] = result.css('a ::attr(href)').extract_first('').replace('"', '')
            heading = result.css('a ::text').extract_first('')
            item['company'] = heading.split('-')[-1].split('|')[0].replace('"', '')
            item['name'] = heading.split('-')[0].replace('"', '') if heading.split('-') else ''

            text = ' '.join(result.css('::text').extract())
            emails = [v for v in text.replace('@ ', '@').split(' ') if '@' in v and '.' in v]
            emails = list(set(emails))
            item['email'] = emails[0] if emails else ''
            item['email'] = item['email'].split(':')[1] if ':' in item['email'] else item['email']
            item['email'] = item['email'][:item['email'].find('.com') + 4] if '.com' in item['email'] else ''
            item['email'] = item['email'].replace('"', '')
            try:
                if (item['email'][0].isnumeric()) or (item['email'][0].isalpha()):

                    item['email'] = item['email']
                else:
                    item['email'] = ''
            except:
                pass
            phones = ', '.join(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)).split(',')

            item['phone'] = phones[0].replace('"', '') if phones else ''
            try:
                if len(item['phone']) > 8:
                    item['phone'] = item['phone'].replace(" ", '')
                else:
                    item['phone'] = ''
            except:
                pass
            item['phone2'] = phones[1].replace('"', '') if len(phones) > 1 else ''
            try:
                if len(item['phone2']) > 8:
                    item['phone2'] = item['phone2'].replace(" ", '')
                else:
                    item['phone2'] = ''
            except:
                pass
            item['industry'] = industry.replace('"', '')
            item['designation'] = designation.replace('"', '')
            items.append(item)

            values_str = '{}("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"),'.format(values_str, item['name'], item['email'],
                                                                               item['phone'], item['phone2'],
                                                                               item['company'], item['city'],
                                                                               item['country'], item['link'],
                                                                               industry, designation)

        if response.css('.rc'):
            self.count += len(response.css('.rc'))
            print('got data: {} total: {}'.format(len(response.css('.rc')), self.count))
            mySql_insert_query = "INSERT IGNORE INTO data (name, email, phone, phone2, company, city, country, link, industry, designation) VALUES {}".format(
                values_str[:-1])
            try:
                self.cursor.execute(mySql_insert_query)
                for item in items:
                    writer.writerow(item)
                    csvfile.flush()
            except Exception as e:
                self.csv_count += len(items)
                print('excel_count: {}'.format(self.csv_count))
                for item in items:
                    writer.writerow(item)
                    csvfile.flush()
                pass
            self.connection.commit()


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
})

process.crawl(GoogleSpider)
process.start()
