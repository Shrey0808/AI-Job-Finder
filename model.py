import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from clean import clean
import numpy as np

def similar(dc, title, skills, salary):
    df = pd.DataFrame(dc)
    df = clean(df)
    df.fillna('', inplace=True)

    # Vectorize the text data
    vectorizer = TfidfVectorizer()
    title_vectors = vectorizer.fit_transform(df['title'].tolist() + [title])
    skills_vectors = vectorizer.fit_transform(df['skills'].tolist() + [skills])

    # Calculate cosine similarity
    title_similarity = cosine_similarity(title_vectors[-1], title_vectors[:-1]).flatten()
    skills_similarity = cosine_similarity(skills_vectors[-1], skills_vectors[:-1]).flatten()

    # Normalize salaries and calculate salary similarity
    scaler = StandardScaler()
    salaries = df['mean_salary'].values.reshape(-1, 1)
    normalized_salaries = scaler.fit_transform(salaries)
    normalized_input_salary = scaler.transform([[salary]])
    salary_similarity = 1 - np.abs(normalized_salaries - normalized_input_salary).flatten()

    # Combine similarities (weighted sum)
    combined_similarity = 0.4 * title_similarity + 0.4 * skills_similarity + 0.2 * salary_similarity

    # Add similarity score to DataFrame and sort by it
    df['similarity_score'] = combined_similarity
    df_sorted = df.sort_values(by='similarity_score', ascending=False)
    return list(df_sorted['index'])

if __name__ == "__main__":
    title = "Data Science"
    skills = "Python, Machine Learning"
    salary = 800000
    dc = pd.read_csv("job.csv").to_dict(orient='list')
    order = similar(dc, title, skills, salary)
    print(order)