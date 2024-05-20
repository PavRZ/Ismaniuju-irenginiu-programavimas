from bs4 import BeautifulSoup as bs
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdriver_path = "C:\\Users\\Augustas\\Desktop\\STUDIJOS 2021\\6 semestras\\Ismaniuju irenginiu programavimas\\React_native_lab\\2 ld failai is moodle\\chromedriver-win32\\chromedriver.exe"
service = Service(executable_path="C:\\Users\\Augustas\\Desktop\\STUDIJOS 2021\\6 semestras\\Ismaniuju irenginiu programavimas\\React_native_programele+IMDB_Search\\imdbSearch_and_mqttBackend\\chromedriver-win64\\chromedriver.exe")

# Options for chromedriver
chrome_options = Options()

driver = webdriver.Chrome(service=service, options=chrome_options)

url="https://data.nordpoolgroup.com/auction/day-ahead/capacities?deliveryDate=latest&deliveryArea=LT"

"""
## Function to get tables data from nordpool website
"""
cookies_handle = False # Handle to check whether cookies have been disabled or not
timezone_handle = False # Handle to check whether timezone was changed or not

def startDriver_cookie():
    global cookies_handle # Globalizing the variable so it could be seen by a function

    # Initializing chromedriver window
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)

    # Statement to check whether cookies have been disabled on first connect, if not - disables them
    if (cookies_handle == False):
        # Wait for the cookies popup to appear
        cookies_popup = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "cdk-overlay-0")))
        # Find the button to disallow cookies
        disallow_button = cookies_popup.find_element(By.XPATH, "//button[contains(text(), 'Disallow and close')]")
        # Click the button to disallow cookies
        disallow_button.click()
        cookies_handle = True

def change_timezone():
    global timezone_handle # Globalizing the variable so it could be seen by a function

    # Statement to check whether timezone of the data has been changed from EET to GMT, if not - changes it
    if (timezone_handle == False):

        # settings_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Settings')]")
        settings_button = driver.find_element(By.ID, "settings-dropdown")
        settings_button.click()

        GMT_button = settings_button.find_element(By.XPATH, "//button[contains(text(), 'GMT')]")
        GMT_button.click()

        settings_button.click()
        time.sleep(1)

        timezone_handle = True

def get_nordpool_info():
    # Getting nordpool HTML code
    nordpool_html = driver.page_source

    # Parsing HTML content using BeautifulSoup
    soup = bs(nordpool_html, "html.parser")
    
    all_tables = soup.find_all('table')

    # print(len(all_tables))  # Shows how many tables there are saved in a variable all_tables

    # Saves table HTML content to a file
    with open("tables.html", "w", encoding="utf-8") as file:
        for table in all_tables:
            file.write(table.prettify())

    return all_tables   # Returns all saved tables from nordpool website in HTML format

"""
## Function to convert HTML table data from nordpool v0.3
"""
def convert_tables_to_json(tables):
    # print(tables[2].prettify())
    one_table_data = [[c.text for c in row.find_all('td')] for row in tables[2].find_all('tr')[:-1]]
        # c.text - text of one cell named c
        # c in row.find_all('td') means - that it goes through all through al found 'td' cells and get their text
        # for row in table[2].find_all('tr') means - that it finds all cell text in ALL found rows of the table
        # [:-1] - doesnt save the last list element of the row because there is no data in it:) 

    # print(one_table_data)
    # print(tables[1])

    one_table_header = [[c.text for c in row.find_all('td')] for row in tables[1].find_all('tr')]
 
    result = [dict(zip(one_table_header[0], row)) for row in one_table_data]    
    # Because there is a list of data rows but only one header row, i merged every data row with a header row using command zip
    # after zipping all the rows it is saved in a dict

    # print(type(result)) # Line to check the type of variable result

    # Saving table data to json file
    result_json = json.dumps(result, indent = 4)    # Transforms zipped Python data to JSON format for SAVING

    with open('table.json', 'w') as file:   # Saving table data to json file
        file.write(result_json)

    return result   # RESULTING result because its type is LIST, result_json is string and it doesnt work when I want to represent the data in Flask web form

def nordpool():
    startDriver_cookie()    # Starting the webdriver service
    change_timezone()       # Changing the timezone of the table data
    tables_html = get_nordpool_info()   # Getting HTML data of the tables
    tables_json = convert_tables_to_json(tables_html)  # Converting HTML table data to JSON format
    return tables_json

# nordpool()