from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from mysql.connector import errorcode
import lxml
from webdriver_manager.chrome import ChromeDriverManager
import html5lib
from datetime import datetime



#Set up current year
YEAR = str(datetime.now().year)
# cert
PATH_TO_CERT='C:/Users/danle/Documents/important/DigiCertGlobalRootG2.crt.pem'


# Pulls all the years from the specific F1 page
def url_pull_years(F1page):
    # Start scraping from html
    options = Options()
    # Run without visual browser pop-up with chrome
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    # Obtain the years for Formula1 data
    years = []
    driver.get(F1page)
    elem = driver.find_elements_by_xpath('//li[@class="resultsarchive-filter-item"]')
    for a in elem:
        content = driver.execute_script('return arguments[0].textContent;',a)
        content= content.strip()
        # If is_num will also work here, but I want to ensure no floating points exist
        # either as a year should only be an int
        try:
            int(content)
        except ValueError:
            break
        years.append(content)
    driver.quit()
    return years

# Pull each table from the website for each given year, the different categories are different tables that can be pulled.
def html_to_df_csvDump(Formula1Years,current_year,cert_path):
    # These categories can be found on this html_start page.  They are the 4 different categories to change the table.
    html_start ='https://www.formula1.com/en/results.html'
    categories = ['races','drivers','team','fastest-laps']
    # We want every category of every year.
    # This is simplest way to do this as we will loop through all 60+ years, and then loop to the next category.
    for cat in categories:
        for year in Formula1Years:
            # As the 2022 year hasn't begun, no values will populate which will cause the script to break
            #if year == '2022':
            #    continue
            new_html = html_start+'/'+year+'/'+cat+'.html'
            try:
                table = pd.read_html(new_html)
            except ValueError:
                continue
            # Since pd.read_html brings up a list of tables on each page, we just want the first iteration.
            # For this web address and all the ones that are utilized
            # through this script there is only 1 table each time we do this.
            df = table[0]
            # Remove index of df
            df['year'] = pd.Series([year for x in range(len(df.index))])
            df.dropna(how='all', axis=1, inplace=True)
            # A few data cleaning if statements depending on which category we are in.
            # Since Pos is entered as an int, we want to make sure EX or DQ are entered as Pos 0 (ie. given no position)
            # Also wanted to split the three different identifiers in the name:
            # First Name, Last Name, and Three letter identifier.
            if cat == 'drivers' or cat == 'fastest-laps':
                df[['FirstName','LastIdentifier']] = df['Driver'].str.split('  ',1,expand=True)
                df[['LastName','Identifier']] = df['LastIdentifier'].str.split('  ',1,expand=True)
                df = df.drop(['Driver','LastIdentifier'],axis=1)
                if cat == 'drivers':
                    df.loc[(df['Pos'] == 'DQ'),'Pos'] = '0'
                else:
                    cat = 'fastestlaps'
            elif cat == 'team':
                df.loc[(df['Pos'] == 'EX'), 'Pos'] = '0'
            elif cat == 'races':
                df[['FirstName', 'LastIdentifier']] = df['Winner'].str.split('  ', 1, expand=True)
                df[['LastName', 'WinningIdentifier']] = df['LastIdentifier'].str.split('  ', 1, expand=True)
                df = df.drop(['Winner', 'LastIdentifier'], axis=1)
            # Prior years to current year should have data finalized already and will not change
            # However current year data will definitely update as it comes in
            if year == current_year:
                ls = list(df.columns)
                print(ls)
                #continue
                config = {
                    'host': 'formula1-full-data.mysql.database.azure.com',
                    'user': 'dmlesper',
                    'password': pswd,
                    'database': 'formula1',
                    'client_flags': [mysql.connector.ClientFlag.SSL],
                    'ssl_ca': cert_path
                }
                try:
                    conn = mysql.connector.connect(**config)
                    print('Connected')
                except mysql.connector.Error as err:
                    print(err)
                else:
                    cursor = conn.cursor()
                    query = """SELECT year FROM {category} WHERE year = {year}""".format(category=cat,year=current_year)
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cursor.close()
                    conn.close()




            else:
                continue
                # Added to sql
                sqlCon = create_engine(
                    'mysql+pymysql://dmlesper:' + pswd + '@formula1-full-data.mysql.database.azure.com:3306/formula1',
                    connect_args={'ssl': {'key': 'whatever'}})
                df.to_sql(con=sqlCon, name=cat, if_exists='append', index=False)
                sqlCon.dispose()

### Main
# URL address creation
formula1_page='https://www.formula1.com/en/results.html'
yrs = url_pull_years(formula1_page)
html_to_df_csvDump(yrs,YEAR,PATH_TO_CERT)


