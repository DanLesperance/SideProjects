import urllib.request as urllib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


this_year = datetime.now().year
# URL address creation
formula1_page = "https://www.formula1.com/en/results.html/2021/races.html"
def url_pull(page):
    # Start scraping from html
    page = urllib.urlopen(page)
    #Run without visual browser pop-up with chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    # Obtain the years for Formula1 data
    years=[]
    driver.get(page)
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
    return years

# Pull each table from the website for each given year, the different categories are different tables that can be pulled.
def html_to_df(Formula1Years):
    html_start ='https://www.formula1.com/en/results.html'
    categories = ['races','drivers','team','fastest-laps']
    for year in Formula1Years:
        for cat in categories:
            new_html = html_start+'/'+year+'/'+cat+'.html'
            table = pd.read_html(new_html)
            df = table[0]
            df['year'] = pd.Series([year for x in range(len(df.index))])
            df.dropna(how='all', axis=1, inplace=True)
            if cat == 'drivers' or cat == 'fastest-laps':
                df[['FirstName','LastIdentifier']] = df['Driver'].str.split('  ',1,expand=True)
                df[['LastName','Identifier']] = df['LastIdentifier'].str.split('  ',1,expand=True)
                df=df.drop(['Driver','LastIdentifier'],axis=1)
            elif cat == 'races':
                df[['FirstName', 'LastIdentifier']] = df['Winner'].str.split('  ', 1, expand=True)
                df[['LastName', 'WinningIdentifier']] = df['LastIdentifier'].str.split('  ', 1, expand=True)
                df = df.drop(['Winner', 'LastIdentifier'], axis=1)
            df.to_csv('Formula1_' + cat + '_' + year + '.csv', index=False)
        break











