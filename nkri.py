from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.chrome.options import Options
import joblib
import time
import random

proxies = joblib.load('proxy.lb')
def get_random_proxy():
    return random.choice(proxies)

chrome_options = Options()
chrome_options.add_argument('--proxy-server=%s' % get_random_proxy())

PATH = r"C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

def init_driver():
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    return driver

def get_job_details(driver, job_link, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            driver.get(job_link)
            wait = WebDriverWait(driver, 10)
            job = {'link': job_link}

            job['title'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
            job['company'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jd-header-comp-name__MvqAI a'))).text
            job['location'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jhc__loc___Du2H span.styles_jhc__location__W_pVs'))).text
            job['experience'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jhc__exp__k_giM span'))).text
            job['salary'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jhc__salary__jdfEC span'))).text.strip()
            job['description'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_JDC__dang-inner-html__h0K4t'))).text
            job['role'] = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Role"]/following-sibling::span/a'))).text
            job['industry_type'] = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Industry Type"]/following-sibling::span/a'))).text
            job['department'] = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Department"]/following-sibling::span/a'))).text
            job['employment_type'] = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Employment Type"]/following-sibling::span/span'))).text
            job['role_category'] = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Role Category"]/following-sibling::span/span'))).text
            job['education'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_education__KXFkO div.styles_details__Y424J'))).text
            tags_elements = driver.find_elements(By.CSS_SELECTOR, 'div.styles_key-skill__GIPn_ a.styles_chip__7YCfG')
            tags = [tag_element.text for tag_element in tags_elements] if tags_elements else []
            job['tags'] = tags

            return job
        except (TimeoutException, StaleElementReferenceException) as e:
            attempt += 1
            print(f"Retry {attempt}/{retries} for job link: {job_link} due to {type(e).__name__}")
            time.sleep(2)  # Adding a small delay before retrying

    return None

def naukri(job_title, location, experience):
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.naukri.com/")
    print("Opened Naukri.com")

    wait = WebDriverWait(driver, 30)
    try:
        job_title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter skills / designations / companies"]')))
        location_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter location"]')))
        experience_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'expereinceDD')))
        print("Found search input fields")
    except TimeoutException:
        print("Search input fields took too long to load!")
        driver.quit()
        return []

    # Enter the job title, location
    job_title_input.send_keys(job_title)
    location_input.send_keys(location)
    
    # Click the experience dropdown to open it
    experience_dropdown.click()

    # Locate the experience option 
    experience_option_xpath = f'//ul[contains(@class, "dropdown")]//span[text()="{experience}"]'
    try:
        experience_option = wait.until(EC.element_to_be_clickable((By.XPATH, experience_option_xpath)))
        experience_option.click()
        print(f"Selected experience: {experience}")
    except TimeoutException:
        print(f"Timeout selecting experience: {experience}")
        driver.quit()
        return []

    # Submit the fields
    job_title_input.send_keys(Keys.RETURN)
    print("Submitted search query")
    jobs = []
    job_links = []
    pages_to_scrape = 3
    current_page = 1

    # Wait for the results page to load
    while current_page <= pages_to_scrape:
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')))
            print("Found job listing elements")
        except TimeoutException:
            print("Job listings took too long to load!")
            break

        # Extract job listings
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')

        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'a.title')
                job_link = title_element.get_attribute('href')
                job_links.append(job_link)
            except NoSuchElementException:
                print("Title not found for one job listing")

        current_page += 1
        if current_page <= pages_to_scrape:
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="styles_btn-secondary__2AsIP"]')))
                next_button.click()
                time.sleep(0.5)
                print(f"Navigating to page {current_page}")
            except TimeoutException:
                print("Next button not found, exiting")
                break

    driver.quit()

    # Use ThreadPoolExecutor to process job links concurrently
    max_workers = 5
    drivers = [init_driver() for _ in range(max_workers)]
    jobs = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {executor.submit(get_job_details, drivers[i % max_workers], link): link for i, link in enumerate(job_links)}
        for future in as_completed(future_to_job):
            link = future_to_job[future]
            try:
                job = future.result()
                if job:
                    jobs.append(job)
            except Exception as exc:
                print(f"Job link {link} generated an exception: {exc}")

    # Close all the driver instances
    for driver in drivers:
        driver.quit()

    return jobs

if __name__ == "__main__":
    # User input
    job_title = 'Data Science'
    location = 'Delhi'
    experience = '15 years'
    start_time = time.time()
    job_listings = naukri(job_title, location, experience)
    end_time = time.time()
    print("Total Runtime:", end_time - start_time)
    print("Total Jobs Found:", len(job_listings))

    # for job in job_listings:
    #     print("=" * 40)
    #     print(f"Title: {job['title']}")
    #     print(f"Company: {job['company']}")
    #     print(f"Location: {job['location']}")
    #     print(f"Experience: {job['experience']}")
    #     print(f"Salary: {job['salary']}")
    #     print(f"Description: {job['description']}")
    #     print(f"Role: {job['role']}")
    #     print(f"Industry Type: {job['industry_type']}")
    #     print(f"Department: {job['department']}")
    #     print(f"Employment Type: {job['employment_type']}")
    #     print(f"Role Category: {job['role_category']}")
    #     print(f"Education: {job['education']}")
    #     print(f"Tags: {', '.join(job['tags'])}")
    #     print(f"Link: {job['link']}")