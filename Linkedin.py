import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep, time

PATH = r"C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

def linkedin(job_titles, locations, exp_lvl):
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)  # Increased wait time

    # Initialize lists to hold job data
    job_data = []

    # Calculate the number of pages to scrape based on the number of jobs
    jobs_per_page = 25
    pages_to_scrape = 1
    if int(exp_lvl) in range(0,3):
        experience_levels = ['Entry level']
    elif int(exp_lvl) in range(3,6):
        experience_levels = ['Associate']
    elif int(exp_lvl) in range(6,11):
        experience_levels = ['Mid-Senior level']
    else:
        experience_levels = ['Director']
    # Define experience level mappings
    experience_map = {
        'Internship': '1',
        'Entry level': '2',
        'Associate': '3',
        'Mid-Senior level': '4',
        'Director': '5'
    }

    def generate_url(job_title, location, experience_code, page):
        return f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&f_E={experience_code}&start={page * jobs_per_page}"

    for job_title in job_titles:
        for experience_level in experience_levels:
            # Ensure provided experience level is valid
            if experience_level not in experience_map:
                print(f"Invalid experience level: {experience_level}")
                continue

            # Fetch corresponding experience level code from mapping
            experience_code = experience_map[experience_level]

            for location in locations:
                for i in range(pages_to_scrape):
                    url = generate_url(job_title, location, experience_code, i)

                    try:
                        driver.get(url)
                        sleep(3)  # Adjust sleep to allow the page to load

                        job_container = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list li')))
                    except TimeoutException:
                        print("Job listings took too long to load!")
                        continue

                    for job_element in job_container:
                        job = {}
                        try:
                            job['title'] = job_element.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').text.strip()
                        except NoSuchElementException:
                            job['title'] = None

                        try:
                            job['url'] = job_element.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
                        except NoSuchElementException:
                            job['url'] = None

                        try:
                            job['company'] = job_element.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle').text.strip()
                        except NoSuchElementException:
                            job['company'] = None

                        try:
                            job['location'] = job_element.find_element(By.CSS_SELECTOR, 'span.job-search-card__location').text.strip()
                        except NoSuchElementException:
                            job['location'] = None

                        # Experience and salary are not directly available on LinkedIn job listings
                        exp_map = {
                            'Entry level': '0-3 years',
                            'Associate': '4-8 years',
                            'Mid-Senior level': '8-12 years',
                            'Director': '12 years'
                        }
                        job['experience'] = exp_map[experience_level]
                        job['salary'] = None

                        # Tags are also not available, we keep it empty
                        job['tags'] = None
                        job['source'] = 'Linkedin'

                        job_data.append(job)

                    sleep(3)  # Adjust sleep to prevent being flagged as a bot

    driver.quit()
    return job_data

if __name__ == "__main__":
    # User input
    job_titles = ['Software Engineer']  # List of job titles
    locations = ['Delhi']  # List of locations
    experience_levels = '10'  # List of experience levels

    start_time = time()
    job_listings = linkedin(job_titles, locations, experience_levels)
    end_time = time()

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
