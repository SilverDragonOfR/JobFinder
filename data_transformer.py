import pandas as pd
import re

# Removes extra spaces
def clean_string(s):
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def transform_jobs_data(all_jobs):
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(all_jobs)

    df.fillna("", inplace=True)
    
    # Normalize string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: clean_string(x) if isinstance(x, str) else x)
    
    # Title-case the location
    if "Location" in df.columns:
        df["Location"] = df["Location"].apply(lambda x: x.title() if x else x)
    
    if "Job Posting Time" in df.columns:
        df["Job Posting Time"] = df["Job Posting Time"].apply(lambda x: clean_string(x) if x else "Not Provided")
    
    # Replace empty descriptions
    if "Job Description" in df.columns:
        df["Job Description"] = df["Job Description"].replace("", "Not Provided")
    
    # Remove non-ASCII chars in title and company
    for col in ["Job Title", "Company"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x)
    
    # Deduplicate by URL or Title+Company
    if "Job URL" in df.columns and df["Job URL"].str.strip().any():
        df = df.drop_duplicates(subset=["Job URL"], keep="first")
    else:
        df = df.drop_duplicates(subset=["Job Title", "Company"], keep="first")
    
    return df