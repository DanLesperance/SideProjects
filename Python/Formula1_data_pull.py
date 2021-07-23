import urllib.request as urllib
from bs4 import BeautifulSoup
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver import ActionChains


this_year = datetime.now().year
# URL address creation
formula1_page = "https://www.formula1.com/en/results.html/2021/races.html"

# Start scraping from html
page = urllib.urlopen(formula1_page)
#Run without visual browser pop-up with chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(chrome_options=options)
# Obtain the years for Formula1 data
years=[]
driver.get(formula1_page)
elem = driver.find_elements_by_xpath('//li[@class="resultsarchive-filter-item"]')
for a in elem:
    content = driver.execute_script('return arguments[0].textContent;',a)
    content= content.strip()
    try:
        int(content)
    except ValueError:
        break
    if content != str(this_year):
        years.append(content)
    else:
        pass
driver.quit()

html_start ='https://www.formula1.com/en/results.html'
categories = ['races','drivers','teams','fastest-laps']
for year in years:
    for cat in categories:
        new_html = html_start+'/'+year+'/'+cat+'.html'
        print(new_html)
        try:
            table = pd.read_html(new_html)
            print(table)
        except ValueError:
            pass










