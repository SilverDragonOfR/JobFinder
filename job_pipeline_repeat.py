import argparse
import os
from dotenv import load_dotenv
from google_extractor import extract_google_jobs
from linkedin_extractor import extract_linkedin_jobs
from data_transformer import transform_jobs_data
from storage import store_to_csv, store_to_sqlite

def run_job_pipeline():
    all_jobs = []

    print("Extracting jobs from Google Jobs via SerpAPI...")
    serpapi_key = os.getenv("SERPAPI_KEY")
    google_jobs = extract_google_jobs("Data Engineer", "United States", serpapi_key)
    print(f"Found {len(google_jobs)} job postings from Google Jobs.")
    all_jobs.extend(google_jobs)

    print("Extracting jobs from LinkedIn...")
    linkedin_jobs = extract_linkedin_jobs("Data Engineer", "United States")
    print(f"Found {len(linkedin_jobs)} job postings from LinkedIn.")
    all_jobs.extend(linkedin_jobs)

    if all_jobs:
        print("Transforming data...")
        df_clean = transform_jobs_data(all_jobs)
        store_to_csv(df_clean)
        store_to_sqlite(df_clean)
    else:
        print("No new job postings found.")

if __name__ == "__main__":
    load_dotenv()
    run_job_pipeline()