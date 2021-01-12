# numbers = []
for num in range(10000000000):
  num=str(num).zfill(10)
  print(num)
# numbers.append(num)
# # x="1"
# #
# #
# # while int(x)<10:
# #     y = x.zfill(5)
# #     print(y)
# #     z=int(y)
# #     z+=1
# #     x=z
# try:
#     import pkg_resources.py2_warn
# except ImportError:
#     pass
#
# import datetime
# import json
# import urllib.request
# import csv
#
# import scrapy
# from scrapy.crawler import CrawlerProcess
#
# csv_columns = ['id', 'description', 'time', 'date', 'location', 'totalPieces']
# # csvfile = open('dhl-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
# # writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
# # writer.writeheader()
#
#
# class Carvana(scrapy.Spider):
#     name = 'dhl'
#     title = 'dhl'
#     start_urls = ['https://www.dhl.com/shipmentTracking?AWB=9649316106&countryCode=g0&languageCode=en&_=1604558819465']
#     all_cars = []
#     CONCURRENT_REQUESTS = 1
#     #
#     @staticmethod
#     def get_dict_value(data, key_list, default=''):
#         """
#         gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
#         :param data: dictionary
#         :param key_list: list of key
#         :param default: return value if key not found
#         :return:
#         """
#         for key in key_list:
#             if data and isinstance(data, dict):
#                 data = data.get(key, default)
#             else:
#                 return default
#         return data
#
#     def start_requests(self):
#         yield scrapy.Request(url='https://www.dhl.com/shipmentTracking?AWB=9649316106&countryCode=g0&languageCode=en&_=1604560412124', callback=self.parse,
#                              headers={"User-Agent": "Chrome/84.0.4147.89"}
#                              # ,meta={"proxy": "https://144.217.101.245:3129"}
#                              )
#
#     def parse(self, response):
#         # for json_str in response.css('script[data-react-helmet="true"][type="application/ld+json"] ::text').extract():
#         #     json_data = json.loads(json_str)
#         htl=urllib.request.urlopen( 'https://www.dhl.com/shipmentTracking?AWB=9649316106&countryCode=g0&languageCode=en&_=1604558819465')
#         json_data=json.load(htl)
#         item = dict()
#         item['id'] = json_data.get('id')
#         item['description'] = json_data.get('description')
#         item['time'] = json_data.get('time')
#         item['date'] = json_data.get('date')
#         item['location'] = json_data.get('location')
#         item['totalPieces'] = json_data.get('totalPieces')
#
#                 # yield {
#                 #     'trim':item['trim']
#                 # }
#                 # for div in response.css('div[data-qa="result-tile"]'):
#                 #     if div.css('g path[fill="#feb948"]') and div.css('a[data-qa="vehicle-link"] ::attr(href)').extract_first('') in item['link']:
#                 #         item['purchasePending'] = True
#                 # # trim=response.css('h4.vehicle-trim.MakeModelTrimstyles__VehicleTrim-sc-1fjrpe9-3.iGMUvV')
#                 # if item['link'] not in self.all_cars:
#                 #     self.all_cars.append(item['link'])
#                 #     writer.writerow(item)
#                 #     csvfile.flush()
#                 #     print('saved: {}'.format(item['link']))
#                 # else:
#                 #     print('duplicate car: {}'.format(item['link']))
#                 #
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(Carvana)
# process.start()
