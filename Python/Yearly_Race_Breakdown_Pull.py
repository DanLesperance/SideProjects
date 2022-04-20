from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import lxml
from webdriver_manager.chrome import ChromeDriverManager
import html5lib
import sys
import time

def html_to_df(html):
    html_df_list = pd.read_html(html)
    html_df = html_df_list[0]
    if html_df.empty:
        print("Empty DF")
        sys.exit(1)
    else:
        return html_df


def main():
    overall_race_df = html_to_df('https://www.formula1.com/en/results.html/2021/races.html')
    grands_prix = list(overall_race_df['Grand Prix'])
    race_num = 1064 # The race number for Bahrain 2021
    for grand_prix in grands_prix:
        per_race_html = 'https://www.formula1.com/en/results.html/2021/races/'+str(race_num)+'/'+grand_prix+'/race-result.html'
        html_to_df(per_race_html)





if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds".format(duration))
