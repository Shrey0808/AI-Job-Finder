from concurrent.futures import ThreadPoolExecutor, as_completed
from naukri import naukri
from internshala import internshala
from Timesjobs import timesjob
from Linkedin import linkedin
import pandas as pd
from clean import *

def fetch_jobs(function, job_title, location, experience):
    return function(job_title, location, experience)


def search(job_title, location, experience):
    job_listings = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_jobs, naukri, job_title, location, experience),
            executor.submit(fetch_jobs, internshala, job_title, location, experience),
            executor.submit(fetch_jobs, timesjob, job_title, location, experience),
            executor.submit(fetch_jobs , linkedin , job_title, location , experience)
        ]
        for future in as_completed(futures):
            job_listings.extend(future.result())

    df = pd.DataFrame(job_listings)
    df = df.dropna(subset=['title','url','company','location'])
    df['index'] = range(1,len(df)+1)
    df.to_csv('job.csv',index=False)
    df = pd.read_csv('job.csv')
    dc = df.to_dict()
    return dc

if __name__ == "__main__":
#   User input
    job_title = ['Data Science']
    location = ['Bangalore']
    experience = '3'
    dc = search(job_title, location, experience)