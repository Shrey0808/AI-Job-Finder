from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

PATH = r"chromedriver.exe"

def timesjob(job_title, location, exp):
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off

    service = Service(PATH)
    driver = webdriver.Chrome(service=service)

    if exp =='1':
        experience = '1 year'
    elif int(exp)>20:
        experience = '20 years'
    else:
        experience = exp + ' years'

    driver.get("https://www.timesjobs.com/")
    
    wait = WebDriverWait(driver, 10)
    try:
        job_title_input = wait.until(EC.presence_of_element_located((By.ID, 'txtKeywords')))
        location_input = wait.until(EC.presence_of_element_located((By.ID, 'txtLocation')))
        experience_dropdown = Select(driver.find_element(By.ID, 'cboWorkExp1'))
    except TimeoutException:
        print("Search input fields took too long to load!")
        driver.quit()
        return []

    job_title_input.send_keys(job_title)
    location_input.send_keys(location)

    try:
        experience_dropdown.select_by_visible_text(experience)
    except TimeoutException:
        print(f"Timeout selecting experience: {experience}")
        driver.quit()
        return []
    
    job_title_input.send_keys(Keys.RETURN)

    jobs = []
    num_pages_to_scrape = 2

    for page in range(1, num_pages_to_scrape + 1):
        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'job-bx')))
            job_elements = driver.find_elements(By.CLASS_NAME, 'job-bx')

            for job_element in job_elements:
                job = {}
                try:
                    title_element = job_element.find_element(By.CSS_SELECTOR, 'header h2 a')
                    job['title'] = title_element.text
                    job['url'] = title_element.get_attribute('href')
                except NoSuchElementException:
                    job['title'] = None
                    job['url'] = None

                try:
                    job['company'] = job_element.find_element(By.CLASS_NAME, 'joblist-comp-name').text.split('\n')[0]
                except NoSuchElementException:
                    job['company'] = None

                try:
                    job['location'] = job_element.find_element(By.CSS_SELECTOR, 'ul.top-jd-dtl li span').text
                except NoSuchElementException:
                    job['location'] = None

                try:
                    experience_element = job_element.find_element(By.XPATH, ".//li[contains(., 'card_travel')]")
                    job['experience'] = experience_element.text.replace('card_travel', '').strip()
                except NoSuchElementException:
                    job['experience'] = None

                try:
                    salary_element = job_element.find_element(By.CSS_SELECTOR, 'ul.top-jd-dtl li i.rupee').find_element(By.XPATH, '..')
                    job['salary'] = salary_element.text
                except NoSuchElementException:
                    job['salary'] = None

                try:
                    job['tags'] = job_element.find_element(By.CSS_SELECTOR, 'ul.list-job-dtl li span.srp-skills').text
                except NoSuchElementException:
                    job['tags'] = None

                job['source'] = 'Timesjobs'

                jobs.append(job)
                
        except:
            print(f"An error occurred while loading job listings:")
            break

        # Locate the pagination button for the next page
        if page < num_pages_to_scrape:
            try:
                next_page_button = driver.find_element(By.XPATH, f"//a[text()='{page + 1}']")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                time.sleep(2)  
                next_page_button.click()
                time.sleep(5)
            except:
                break

    driver.quit()
    return jobs

if __name__ == "__main__":
    # User input
    job_title = ['Data Science', 'Machine Learning']
    location = ['Delhi']
    experience = '21'
    start_time = time.time()
    job_listings = timesjob(job_title, location, experience)
    end_time = time.time()
    print("Total Runtime:", end_time - start_time)
    print("Total Jobs Found:", len(job_listings))
    # for job in job_listings:
    #     print(f"Title: {job['title']}")
    #     print(f"Company: {job['company']}")
    #     print(f"Location: {job['location']}")
    #     print(f"Experience: {job['experience']}")
    #     print(f"Salary: {job['salary']}")
    #     print(f"Tags: {job['tags']}")
    #     print(f"URL: {job['url']}")
    #     print("-" * 40)