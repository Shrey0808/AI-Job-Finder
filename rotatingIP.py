from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import joblib

# Set up the WebDriver (this example uses Chrome)
PATH = r"C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
service = Service(PATH)
driver = webdriver.Chrome(service=service)

def get_proxy():
    url = "https://free-proxy-list.net/"
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    proxies = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols:
            proxies.append(cols[0].text)
    driver.quit()
    return proxies


proxies = get_proxy()
joblib.dump(proxies, 'proxy.lb')
