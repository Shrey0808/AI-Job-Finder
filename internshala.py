from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

PATH = r"C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

import time
    


def internshala(job_title, location, experience):
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    base_url = "https://internshala.com/"

    if int(experience)>5:
        experience = '5plus'

    def generate_url(job_categories, locations, experience=None):
        if experience is None or experience == 0:
            job_type = "fresher-jobs"
        else:
            job_type = "jobs"
        
        def format_for_url(text):
            return text.lower().replace(" ", "-")
        
        job_categories_part = ",".join(format_for_url(category) for category in job_categories)
        
        locations_part = ",".join(format_for_url(location) for location in locations)
        
        if experience is None or experience == 0:
            url = f"{base_url}{job_type}/{job_categories_part}-jobs-in-{locations_part}/"
        else:
            url = f"{base_url}{job_type}/{job_categories_part}-jobs-in-{locations_part}/experience-{experience}/"

        return url
    
    url = generate_url(job_title, location, experience)

    try:
        driver.get(url)
    except:
        pass
    
    wait = WebDriverWait(driver, 30)
    try:
        close_button = wait.until(EC.element_to_be_clickable((By.ID, 'close_popup')))
        close_button.click()
    except:
        driver.quit()
        return []

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.individual_internship')))
        print("Found job listing elements")
    except :
        print("Job listings took too long to load!")
        driver.quit()
        return []

    jobs = []
    job_listings = driver.find_elements(By.CSS_SELECTOR, '.individual_internship')

    for job_element in job_listings[1:]:
        job = {}
        try:
            job['title'] = job_element.find_element(By.CSS_SELECTOR, '.job-internship-name').text
        except NoSuchElementException:
                job['title'] = None
        
        try:
            company_element = job_element.find_element(By.CSS_SELECTOR, '.company-name')
            job['company'] = company_element.text
        except :
            job['company'] = None

        try:
            location_element = job_element.find_element(By.CSS_SELECTOR, '.locations')
            job['location'] = location_element.text
        except :
            job['location'] = None


        try:
            experience_element = job_element.find_element(By.CSS_SELECTOR, '.ic-16-briefcase + .item_body')
            job['experience'] = experience_element.text
        except :
            job['experience'] = None


        try:
            salary_element = job_element.find_element(By.CSS_SELECTOR, '.ic-16-money + span')
            job['salary'] = salary_element.text
        except :
            job['salary'] = None
        try:
            relative_link = job_element.get_attribute('data-href')
            job['url'] = base_url + relative_link
        except :
            job['url'] = None
            

        job['tags'] = None

        job['source'] = 'Internshala'

        jobs.append(job)

    driver.quit()
    return jobs


if __name__ == "__main__":
    # User input
    job_title = ['Data Science','Machine Learning'] # List of jobs
    location = ['Delhi'] # List of Locations
    experience = '12' # Valid options are Fresher, 1,2,3,4,5,5plus
    start_time = time.time()
    job_listings = internshala(job_title, location, experience)
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
    #     print(f"URL: {job['link']}")
    #     print("-" * 40)

