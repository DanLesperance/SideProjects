from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from sqlalchemy import create_engine



def url_pull(F1page):
    # Start scraping from html
    options = Options()
    # Run without visual browser pop-up with chrome
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    # Obtain the years for Formula1 data
    years = []
    driver.get(F1page)
    elem = driver.find_elements_by_xpath('//li[@class="resultsarchive-filter-item"]')
    for a in elem:
        content = driver.execute_script('return arguments[0].textContent;',a)
        content= content.strip()
        try:
            int(content)
        except ValueError:
            break
        years.append(content)
    driver.quit()
    return years

# Pull each table from the website for each given year, the different categories are different tables that can be pulled.
def html_to_df_csvDump(Formula1Years,sqlCon):
    html_start ='https://www.formula1.com/en/results.html'
    categories = ['races','drivers','team','fastest-laps']
    for cat in categories:
        for year in Formula1Years:
            new_html = html_start+'/'+year+'/'+cat+'.html'
            try:
                table = pd.read_html(new_html)
            except ValueError:
                break
            df = table[0]
            df['year'] = pd.Series([year for x in range(len(df.index))])
            df.dropna(how='all', axis=1, inplace=True)
            if cat == 'drivers' or cat == 'fastest-laps':
                df[['FirstName','LastIdentifier']] = df['Driver'].str.split('  ',1,expand=True)
                df[['LastName','Identifier']] = df['LastIdentifier'].str.split('  ',1,expand=True)
                df=df.drop(['Driver','LastIdentifier'],axis=1)
                if cat == 'drivers':
                    df.loc[(df['Pos'] == 'DQ'),'Pos'] = '0'
            elif cat == 'team':
                df.loc[(df['Pos'] == 'EX'), 'Pos'] = '0'
            elif cat == 'races':
                df[['FirstName', 'LastIdentifier']] = df['Winner'].str.split('  ', 1, expand=True)
                df[['LastName', 'WinningIdentifier']] = df['LastIdentifier'].str.split('  ', 1, expand=True)
                df = df.drop(['Winner', 'LastIdentifier'], axis=1)
            df.to_sql(con=sqlCon, name=cat, if_exists='append')
            #if year == '2021':
                #df.to_csv('Formula1_' + cat + '.csv', index=False)
            #else:
                #df.to_csv('Formula1_' + cat + '.csv', index=False,mode='a',header=False)



### Main
# URL address creation
formula1_page = "https://www.formula1.com/en/results.html/2021/races.html"
sqlEngine = create_engine('mysql+pymysql://root:B1ology!@localhost:3306/formula1_data_dl')
#yrs = url_pull(formula1_page)
#html_to_df_csvDump(yrs,sqlEngine)
yr=['2021']
html_to_df_csvDump(yr,sqlEngine)
sqlEngine.dispose()
