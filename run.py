from flask import Flask, render_template, url_for, redirect, request, session
from main import *
import pandas as pd
from model import *

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html",)

@app.route("/job_list")
def job_list():
    file_path = r"job.csv"
    df = pd.read_csv(file_path)
    jobs = df.to_dict()

    jobs_per_page = 20
    page = request.args.get('page', 1, type=int)
    total_jobs = len(jobs['title'])
    total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

    start = (page - 1) * jobs_per_page
    end = start + jobs_per_page
    paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

    return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages)

@app.route("/srch")
def srch():
    job_title = ['Data Science']
    location = ['Bangalore']
    experience = '3'
    jobs = search(job_title, location, experience)
    df = pd.DataFrame(jobs)
    df.to_csv('job.csv')

    jobs_per_page = 20
    page = request.args.get('page', 1, type=int)
    total_jobs = len(jobs['title'])
    total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

    start = (page - 1) * jobs_per_page
    end = start + jobs_per_page
    paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

    return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages)

@app.route("/aisort")
def aisort():
    df =  pd.read_csv('job.csv')
    dt = df.to_dict(orient='list')
    title = 'Data Science'
    skills = 'Data Science Machine Learning SQL'
    salary = 800000
    order = similar(dt, title, skills, salary)
    print(order)
    df = df.loc[df['index'].isin(order)].set_index('index').loc[order].reset_index()
    jobs = df.to_dict()

    jobs_per_page = 20
    page = request.args.get('page', 1, type=int)
    total_jobs = len(jobs['title'])
    total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

    start = (page - 1) * jobs_per_page
    end = start + jobs_per_page
    paginated_jobs = {key: {k: v for k, v in value.items() if start <= k < end} for key, value in jobs.items()}

    return render_template('job_list.html', jobs=paginated_jobs, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)