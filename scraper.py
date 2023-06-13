

from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
 
options = Options()
# TODO: Will make it headless later
#options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
page_no = 1
url = "http://www.collegescholarships.org/financial-aid/"
browser.get(url)

gender=WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="inline-filter"]/a[1]')))
browser.execute_script("arguments[0].click();", gender)

gender_female =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gender_female"]')))
browser.execute_script("arguments[0].click();", gender_female)

ok_button =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="apply-filters"]')))
browser.execute_script("arguments[0].click();", ok_button)


apply_filter =WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="apply-filter"]')))
browser.execute_script("arguments[0].click();", apply_filter)

awards = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="scholarship-list"]//div[@class="row"]//div[@class="scholarship-summary"]/p/span[@class="lead"]/strong')))
deadlines = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="scholarship-list"]//div[@class="row"]//div[@class="scholarship-summary"]/p/strong')))
links = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="scholarship-list"]//div[@class="row"]//div[@class="scholarship-summary"]/a')))

study_levels = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']/ul/li[2]/span[@class='trim']")))
subjects = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']/ul/li[3]/span[@class='trim']")))
scholarship_name = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='scholarship-list']//div[@class='row']//div[@class='scholarship-description']//h4/a")))

scholarships = []

for i in range(0,len(scholarship_name)):
    scholarship = {}
    scholarship["name"] = scholarship_name[i].text
    scholarship["study_level"] = study_levels[i].text
    scholarship["amount"] = awards[i].text
    scholarship["subject"] = subjects[i].text
    scholarship["deadline"] = deadlines[i].text
    scholarship["link"] =  links[i].get_attribute('href')
    scholarships.append(scholarship)

for s in scholarships:
    browser.get(s["link"])
    time.sleep(1)
    element = browser.find_element(By.XPATH, "//div[@id='description']//a[@class='btn btn-primary' and text()='Apply Online']")
    desc = browser.find_element(By.XPATH, '//*[@id="description"]/p[1]').text
    s["link"] =  element.get_attribute('href')
    s["description"] = desc
print(scholarships)