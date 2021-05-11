import requests
import json
from datetime import datetime

class Management:
    host = 'http://localhost:3080/API/'
    # appKey = 'siggaApiUnb'
    appKeyHash = '76761001f00b44382fe5c23b00dce91f2249c7d354af1cc40f3ff539fd8abfd0'
    timeNow = ''

    def __init__(self):
        now = datetime.now()
        self.timeNow = now.strftime("%d/%m/%Y %H:%M:%S")

    def headers(self):
        return {
            # 'Access-Control-Allow-Origin': '*',
            # 'Connection': 'Keep-Alive',
            # 'Transfer-Encoding': 'chunked',
            'Content-Type': 'application/json'
        }

    def sendToApi(self, url, name, data):
        print(self.host+url)
        response = requests.get(self.host+url, data=json.dumps({name: data, 'updateTime' : self.timeNow, 'appKey': self.appKeyHash}), headers = self.headers())
        self.dataBackup({name: data, 'updateTime' : self.timeNow, 'appKey': self.appKeyHash})
        print('HTTP response: '+ str(response))
        return 1
        ''' 
            STATUS CODES:
                1 - Crawler is running
                2 - Departments attempt to Update 
                3 - Diciplines attempt to update
                4 - finish run and waiting to the next execution time
        '''
    def updateCrawlerStatus(self, status):
        # data = 
        # data = json.dumps(data)
        # print(data)
        
        response = requests.get(self.host+'status', data=json.dumps({'CrawlerStatus' : status, 'updateTime' : str(self.timeNow), 'appKey': self.appKeyHash}), headers = self.headers())
        
        print('HTTP response: '+ str(response))
        
        self.dataBackup({'CrawlerStatus' : status, 'updateTime' : self.timeNow, 'appKey': self.appKeyHash})

        return 1

    def dataBackup(self, data):
        with open('dataBackup.txt', 'a') as f:
            f.write(json.dumps(data))
