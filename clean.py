import pandas as pd
import re

def clean_salary(salary):
    if pd.isna(salary) or (salary in ["Competitive salary" , "Not disclosed" , "Unpaid",]):
        return None,None

    elif "Lacs p.a." in salary:
        clean_salary = re.search(r'Rs (\d+\.\d+) - (\d+\.\d+) Lacs p\.a\.', salary)
        if clean_salary:
            low = float(clean_salary.group(1))
            high = float(clean_salary.group(2))

            low_inr = int(low * 100000)
            high_inr = int(high * 100000)
            return low_inr, high_inr
    elif "Lacs PA" in salary:
        salary = re.sub(r'[^\d\.,-]', '', salary).replace("\n", "").strip()
        parts = salary.split('-')
        return float(parts[0])*100000 , float(parts[1])*100000
    else:

        salary = re.sub(r'[^\d\.,-]', '', salary).replace("\n", "").strip()

        parts = salary.split('-')
        cleaned_parts = []
        for part in parts:
            if ',' in part:
                part = part.replace(',', '')
            cleaned_parts.append(part.strip())
        return float(cleaned_parts[0]), float(cleaned_parts[1])
    
def clean_tag(tag):
    if pd.isna(tag):
        return None
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned_tag = re.sub(r'[^a-zA-Z0-9\s]', '', tag).lower()
    return cleaned_tag.strip() if cleaned_tag else None

def clean(df):
    salary_lower_range , salary_higher_range = [],[]
    for salary in df['salary']:
        clean = clean_salary(salary)
        salary_lower_range.append(clean[0])
        salary_higher_range.append(clean[1])

    cleaned_tags = [clean_tag(tag) for tag in df['tags']]

    cleaned = {
        'title':df['title'],
        'company':df['company'],
        'lower_salary':salary_lower_range,
        'upper_salary':salary_higher_range,
        'skills':cleaned_tags,
        'source':df['source']
    }

    return pd.DataFrame(cleaned)


if __name__ =='__main__':
    df = pd.read_csv('data.csv')
    cleaned_df = clean(df)
    cleaned_df.to_csv('cleaned_df.csv', index=False)