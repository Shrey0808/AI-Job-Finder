# Project Description: AI Job Recommender

## Abstract:
This project involves building an AI job recommender system that scrapes jobs from multiple websites in real-time, processes and stores the job data, and then publishes it on a my own designed website. The system allows users to input job titles, locations, and experience levels to fetch relevant jobs. Additionally, an AI recommender feature utilizes machine learning to provide personalized job recommendations.

## Table of Contents:
1. Introduction
2. Data Collection
3. Data Preprocessing
4. Website Structure
5. AI Recommender Model
6. Usage Instructions
7. Results
8. Conclusion

## 1. Introduction:
The AI Job Recommender system aims to streamline the job search process by aggregating job listings from various platforms such as LinkedIn, Internshala, Timesjob, and Naukri.com. The project encompasses web scraping, data cleaning, and machine learning to deliver personalized job recommendations to users based on their inputs.

## 2. Data Collection:
The system scrapes job data from multiple websites in real-time. The job data includes job titles, locations, experience , skills-required , salary offered and application url. The websites targeted for scraping are:
- LinkedIn
- Internshala
- Timesjob
- Naukri.com

## 3. Data Preprocessing:
Data preprocessing involves cleaning and storing the scraped job data to ensure it is in a suitable format for analysis and display on the website. The preprocessing steps include:
- Removing duplicates and irrelevant job postings.
- Standardizing job titles and location names.
- Storing the cleaned data in a database (MongoDB).

## 4. Website Structure:
The website allows users to input job title, location, and experience level. The structure includes:
- Input fields for job title, location, and experience.
- Search button to fetch jobs in real-time.
- Five filters for viewing all jobs at once or each job on a separate page.
- AI recommender button for personalized job recommendations.

## 5. AI Recommender Model:
The AI recommender system converts user inputs and fetched jobs into vectors and applies cosine similarity to find the most relevant jobs. The model includes:
- Vectorization of job titles, locations, and experience levels.
- Calculation of cosine similarity between user input and job listings.
- Sorting of job listings based on the recommendation score.


## 6. Usage Instructions:
1. **Enter job title**, job location, and experience in the input fields.
2. **Click the search button** to fetch jobs in real-time from LinkedIn, Internshala, Timesjob, and Naukri.com.
3. **Use filters** to view all jobs at once or each job on a separate page.
4. **Click the AI recommender button** to get personalized job recommendations based on cosine similarity.

## 7. Results:
The AI recommender system provides personalized job recommendations by leveraging machine learning techniques to match user inputs with relevant job listings. The recommendations are ranked based on their similarity scores.

## 9. Conclusion:
The AI Job Recommender project offers a comprehensive solution for job seekers by aggregating job listings from multiple platforms and providing personalized recommendations. This project demonstrates the effective use of web scraping, data preprocessing, and machine learning in building a practical and user-friendly application.

---
