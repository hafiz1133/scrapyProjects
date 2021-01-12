import scrapy
import datetime
import json
from scrapy.crawler import CrawlerProcess
import csv
csv_columns = ['name', 'model','year','techName', 'type','finale']
csvfile = open('Tempdata-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()
class Osarm(scrapy.Spider):
    name = 'osarm'
    def start_requests(self):
        yield scrapy.Request(url='https://api-vlrg.osram.info/cars/lookups?kind_id=1&lang=en&lookuptype=manufacturers',callback=self.parse)
    def parse(self, response):
       jsonObj=json.loads(response.text)
       lenght=len(jsonObj)
       for i in range(lenght):
           id=jsonObj[i].get('id')
           name=jsonObj[i].get('name')

           yield scrapy.Request(url='https://api-vlrg.osram.info/cars/lookups?lookuptype=years&lang=en&manufacturer_id='+str(id),callback=self.getDate,meta={'id':id,'name':name})
    def getDate(self,response):
        jsonObj = json.loads(response.text)
        lenght = len(jsonObj)
        for i in range(lenght):
            date = jsonObj[i].get('id')
            id=response.meta['id']
            yield scrapy.Request(
                url='https://api-vlrg.osram.info/cars/lookupmodelvariant?kind_id=1&lookuptype=models&lang=en&manufacturer_id=' + str(
                    id+'&constructionyear='+str(date)), callback=self.parse1,meta={'date':date,'name':response.meta['name']})
    def parse1(self,response):
        date=response.meta['date']
        jsonObj = json.loads(response.text)
        lenght = len(jsonObj)
        for i in range(lenght):
            modelid = jsonObj[i].get('model_id')
            model = jsonObj[i].get('model_name')
            type=jsonObj[i].get('variant_name')
            modelname = model + ' ' + type
            variant_id = jsonObj[i].get('variant_id')
            yield scrapy.Request(url='https://api-vlrg.osram.info/cars/lookuptypeinfo?lang=en&variant_id='+str(variant_id)+'&model_id='+str(modelid)+'&constructionyear'+str(date),callback=self.parse2,meta={'name':response.meta['name'],'date':response.meta['date'],'modelname':modelname})
    def parse2(self,response):
        jsonObj = json.loads(response.text)
        lenght = len(jsonObj)
        for i in range(lenght):
            carid = jsonObj[i].get('id')
            t1=jsonObj[i].get('name')
            t2=jsonObj[i].get('type_kw') + str('kw')
            type= t1+' '+t2

            yield scrapy.Request(url='https://api-vlrg.osram.info/bulbs/positions?car_id='+str(carid)+'&lang=en',callback=self.parse3,meta={'car_id':carid,'name':response.meta['name'],'date':response.meta['date'],'modelname':response.meta['modelname'],'type':type})
    def parse3(self,response):
        car_id = response.meta['car_id']
        jsonObj = json.loads(response.text)
        length=len(jsonObj)
        for i in range(length):
            usename=jsonObj[i].get('use_name')
            if usename == 'Low beam':
                useid=jsonObj[i].get('use_id')
                usename = 'Low beam'
            elif usename == 'High beam':
                useid=jsonObj[i].get('use_id')
                usename = 'High beam'
            elif usename == 'Fog lamps':
                useid=jsonObj[i].get('use_id')
                usename = 'Fog lamps'
            yield scrapy.Request(url='https://api-vlrg.osram.info/bulbs/technologies?car_id='+str(car_id)+'&use_id='+str(useid)+'&lang=en',callback=self.parse4,meta={'cid':car_id,'uid':useid,'usename':usename,'name':response.meta['name'],'date':response.meta['date'],'modelname':response.meta['modelname'],'type':response.meta['type']})
    def parse4(self,response):
        cid=response.meta['cid']
        uid=response.meta['uid']
        usename=response.meta['usename']
        jsonObj = json.loads(response.text)
        length = len(jsonObj)
        for i in range(length):
            techId = jsonObj[i].get('technology_id')
            techName= jsonObj[i].get('tech_name')
            yield scrapy.Request(url='https://api-vlrg.osram.info/bulbs/pillars?car_id='+str(cid)+'&use_id='+str(uid)+'&technology_id='+str(techId)+'&lang=en',callback=self.parse5,meta={'usename':usename,'name':response.meta['name'],'date':response.meta['date'],'modelname':response.meta['modelname'],'type':response.meta['type'],'techName':techName})

    def parse5(self,response):
        jsonOBJ = json.loads(response.text)
        length=len(jsonOBJ)
        count = 0

        item=dict()
        item['name']= response.meta['name']
        item['year']=  response.meta['date']
        item['model']=  response.meta['modelname']
        item['type']= response.meta['type']
        item['techName']=response.meta['techName']
        usename = response.meta['usename']
        ece=jsonOBJ[0].get('ece')
        item['finale']=usename+ ": "+ece
        print('-----')
        writer.writerow(item)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Osarm)
process.start()
