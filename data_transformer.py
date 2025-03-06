import pandas as pd
import re

def clean_string(s):
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def transform_jobs_data(all_jobs):
    df = pd.DataFrame(all_jobs)

    df.fillna("", inplace=True)
    
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: clean_string(x) if isinstance(x, str) else x)
    
    if "Location" in df.columns:
        df["Location"] = df["Location"].apply(lambda x: x.title() if x else x)
    
    if "Job Posting Time" in df.columns:
        df["Job Posting Time"] = df["Job Posting Time"].apply(lambda x: clean_string(x) if x else "Not Provided")
    
    if "Job Description" in df.columns:
        df["Job Description"] = df["Job Description"].replace("", "Not Provided")
    
    for col in ["Job Title", "Company"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x)
    
    if "Job URL" in df.columns and df["Job URL"].str.strip().any():
        df = df.drop_duplicates(subset=["Job URL"], keep="first")
    else:
        df = df.drop_duplicates(subset=["Job Title", "Company"], keep="first")
    
    return df