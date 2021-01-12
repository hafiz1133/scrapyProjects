import json
import datetime

from scrapy.crawler import CrawlerProcess
import csv
# html = requests.get(
#     'https://www.dhl.com/shipmentTracking?AWB=9649316106&countryCode=g0&languageCode=en&_=1604560412124')
# data = json.load(html)
# print("hello")
# print(data)
import scrapy
from scrapy.crawler import CrawlerProcess

csv_columns = ['id', 'time', 'Destination Service Area','Origin Service Area', 'date', 'TotalPieces', 'Status']
csvfile = open('dhl-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


class Dhl(scrapy.Spider):
    name = 'dhl'
    DOWNLOAD_TIMEOUT = 300
    CONCURRENT_REQUESTS = 1

    @staticmethod
    def get_dict_value(data, key_list, default=''):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def start_requests(self):
        # numbers = []
        for num in range(10000000000):
            num = str(num).zfill(10)
        # numbers.append(num)
            url = 'https://www.dhl.com/shipmentTracking?AWB=' + str(num)
            yield scrapy.Request(url=url)

    def parse(self, response):
        item = dict()
        json_data = json.loads(response.text)
        if self.get_dict_value(json_data, ['results']):
            try:
                item['id'] = self.get_dict_value(json_data, ['results'])[0].get('id')
            except:
                item['id']= ""
            try:
                 item['time'] = self.get_dict_value(json_data, ['results'])[0]['checkpoints'][0].get('time')
            except:
                item['time']= ""
            try:
                item['Destination Service Area'] = self.get_dict_value(json_data, ['results'])[0]['destination'].get('value')
                item['Origin Service Area'] = self.get_dict_value(json_data, ['results'])[0]['origin'].get('value')
            except:
                item['Destination Service Area']= ""
            try:
                item['Origin Service Area'] = self.get_dict_value(json_data, ['results'])[0]['origin'].get('value')
            except:
                item['Origin Service Area']=""
            try:
                item['date'] = self.get_dict_value(json_data, ['results'])[0]['checkpoints'][0].get('date')
            except:
                item['date']= ""
            try:
                item['TotalPieces'] = self.get_dict_value(json_data, ['results'])[0]['checkpoints'][0].get('totalPieces')
            except:
                item['TotalPieces']= ""
            try:
                item['Status'] = self.get_dict_value(json_data, ['results'])[0]['delivery'].get('status')
            except:
                item['Status']= ""

            writer.writerow(item)
            # yield scrapy.Request(callback=self.start_requests)
        else:
            pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Dhl)
process.start()
