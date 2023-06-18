from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
dbName = os.getenv('DB_NAME')
collectionName = os.getenv('COLLECTION_NAME')
no_of_pages = os.getenv('NO_OF_PAGES')
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client[dbName]
collection = db[collectionName]

options = Options()
# TODO: Will make it headless later
options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
browser2 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

page_no = 1
finalScholarships = []

while page_no < int(no_of_pages):
    scholarships = []
    url = "http://www.collegescholarships.org/financial-aid/?page="+str(page_no)
    browser.get(url)
    print("Page No:"+str(page_no))
    time.sleep(2)

    if page_no == 1:
        gender=WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="inline-filter"]/a[1]')))
        browser.execute_script("arguments[0].click();", gender)

        gender_female =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gender_female"]')))
        browser.execute_script("arguments[0].click();", gender_female)

        ok_button =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="apply-filters"]')))
        browser.execute_script("arguments[0].click();", ok_button)

        apply_filter =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="apply-filter"]')))
        browser.execute_script("arguments[0].click();", apply_filter)

    deadlines = WebDriverWait(browser, 300).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="scholarship-list"]//div[@class="row"]//div[@class="scholarship-summary"]/p/strong')))
    links = WebDriverWait(browser, 300).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="scholarship-list"]//div[@class="row"]//div[@class="scholarship-summary"]/a')))

    study_levels = WebDriverWait(browser, 300).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']/ul/li[2]/span[@class='trim']")))
    subjects = WebDriverWait(browser, 300).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']/ul/li[3]/span[@class='trim']")))
    scholarship_name = WebDriverWait(browser, 300).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']//h4/a")))


    for i in range(0,len(scholarship_name)):
        scholarship = {}
        scholarship["name"] = scholarship_name[i].text
        scholarship["study_level"] = study_levels[i].text
        scholarship["subject"] = subjects[i].text
        scholarship["deadline"] = deadlines[i].text
        scholarship["link"] =  links[i].get_attribute('href')
        scholarships.append(scholarship)

    for s in scholarships:
        browser2.get(s["link"])
        time.sleep(1)
        element = browser2.find_element(By.XPATH, "//div[@id='description']//a[@class='btn btn-primary' and text()='Apply Online']")
        desc = browser2.find_element(By.XPATH, '//*[@id="description"]/p[1]').text
        amount = 'Not Available'
        try:
            amountEle = browser2.find_element(By.XPATH, '//dt[contains(text(), "Average award:")]/following-sibling::dd')
            amount = amountEle.text
            print(amount)
        except NoSuchElementException:
            try:
                print('Average Amount couldnt be scraped, moving with max')
                amountEle = browser2.find_element(By.XPATH, '//dt[contains(text(), "Max. award:")]/following-sibling::dd')
                amount = amountEle.text
                print(amount)
            except NoSuchElementException:
                try:
                    print('Max Amount couldnt be scraped, moving with min')
                    amountEle = browser2.find_element(By.XPATH, '//dt[contains(text(), "Min. award:")]/following-sibling::dd')
                    amount = amountEle.text
                    print(amount)
                
                except NoSuchElementException:
                    print("No amount found for "+s["name"])

        s["link"] =  element.get_attribute('href')
        s["description"] = desc
        s["amount"] = amount
    finalScholarships.extend(scholarships)
    page_no += 1

scholarshipData = {}
scholarshipData["scholarships"] = finalScholarships
collection.replace_one({}, scholarshipData, upsert=True)
