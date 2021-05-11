import requests
from bs4 import BeautifulSoup
import re
import time
import json
from Management import Management
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
import os
import sys

class Sigaa:
    baseUrl = 'https://sig.unb.br'
    url = 'https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf'

    spiderName = 'SIGAA'
    spiderId = '1'
    Management = ()

    def __init__(self):
        self.Management = Management()
        self.Management.updateCrawlerStatus(1)
        

    def getCoursesByDepartments(self, departmentId):
        response = driver.execute_script("return document.body.outerHTML;")
        bs4 = BeautifulSoup(response, 'html.parser')
        
        coursesList = ''
        if bs4 != None: 
            coursesList = bs4.select('#formListagemComponentes > table > tbody > tr')

        Courses = []
        index = 0
        if(coursesList == []):
            return 
        
        for course in coursesList:
            courseCode = course.select_one('td:nth-child(1)').get_text(strip = True)
            courseName = course.select_one('td:nth-child(2)').get_text(strip = True)
            courseType = course.select_one('td:nth-child(3)').get_text(strip = True)
            courseTotalHours = course.select_one('td:nth-child(4)').get_text(strip = True)
            
            Courses.append({'code': courseCode, 'name': courseName, 'type': courseType, 'totalHours': courseTotalHours, 'departmentId': departmentId})
            index +=1


        self.Management.sendToApi('courses', 'courses', Courses)
        self.Management.updateCrawlerStatus(2)
        

        return Courses

    def getDepartments(self, driver):
        # browserParams = self.getBrowserParams()
        # response = requests.get(self.url+'?nivel=G&aba=p-graduacao', headers=browserParams['headers'], cookies=browserParams['cookies'])
        driver.get(self.url+'?nivel=G&aba=p-graduacao')
        response = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        print(self.url+'?nivel=G&aba=p-graduacao')
        print(response)
        print('what')
        bs4 = BeautifulSoup(response, 'html.parser')
        
        departmentsList = []
        if bs4 != None: 
            departmentsList = bs4.select('#form\:unidades > option')
        
        Departments = []
        index = 0
        for department in departmentsList:
            Departments.append({'id': department.attrs['value'], 'name': department.get_text(strip=True)}) 
            index +=1

        self.Management.sendToApi('departments', 'departments', Departments)
        self.Management.updateCrawlerStatus(2)
        return Departments

    def getBrowserParams(self):
        params = {}

        params['cookies'] = {
            '_ga': 'GA1.2.571145815.1617082802',
            '_gid': 'GA1.2.984949074.1617082802',
            'JSESSIONID': '107A2113DC2E739D39AFE0A086D409BB.sigaa08',
            '_gat': '1',
        }

        params['headers'] = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Origin': self.baseUrl,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': self.url,
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        }
        return params

Spider = Sigaa()


driverPatch = ''
chrome_options = Options()
if(sys.platform == 'linux'):
    driverPatch = './linuxWebDriver/'
    chrome_options.add_argument("--no-sandbox") # linux only
elif(sys.platform == 'win32'):
    driverPatch = './windowsWebDriver/'

chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options , executable_path = driverPatch+'chromedriver.exe')
DepartmentsList = Spider.getDepartments(driver)

driver.get(Spider.url)

graduationLevelOptions = Select(WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#form\:nivel'))))
graduationLevelOptions.select_by_value('G')

print('1')
print(DepartmentsList)
index = -1
for department in DepartmentsList:
    
    print('2')
    index+=1
    if(index == 0):
        continue

    print('3')
    graduationByDepartment = Select(WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#form\:unidades'))))
    graduationByDepartment.select_by_value(department['id'])
    WebDriverWait(driver, 6).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#form\:btnBuscarComponentes'))).click()

    print('4')
    time.sleep(3)

    print('5')
    CoursesList = Spider.getCoursesByDepartments(department['id'])

    time.sleep(3)

    print('6')
driver.quit()