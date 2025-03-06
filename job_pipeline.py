import argparse
from dotenv import load_dotenv
from google_extractor import extract_google_jobs
from linkedin_extractor import extract_linkedin_jobs
from data_transformer import transform_jobs_data
from storage import store_to_csv, store_to_sqlite

def main(args):
    
    all_jobs = []
    
    if args.source in ["google", "both"]:
        print("Extracting jobs from Google Jobs via SerpAPI...")
        google_jobs = extract_google_jobs(args.query, args.location)
        print(f"Found {len(google_jobs)} job postings from Google Jobs.")
        all_jobs.extend(google_jobs)
    
    if args.source in ["linkedin", "both"]:
        print("Extracting jobs from LinkedIn...")
        linkedin_jobs = extract_linkedin_jobs(args.query, args.location)
        print(f"Found {len(linkedin_jobs)} job postings from LinkedIn.")
        all_jobs.extend(linkedin_jobs)
    
    if all_jobs:
        print("Transforming data...")
        df_clean = transform_jobs_data(all_jobs)
        print("Data transformation complete.")
    
        if args.output in ["csv", "both"]:
            store_to_csv(df_clean)
        if args.output in ["sqlite", "both"]:
            store_to_sqlite(df_clean)
    else:
        print("No job data was extracted.")


if __name__ == "__main__":
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Job Data Pipeline: Extract Data Engineer job postings from Google Jobs & LinkedIn")
    parser.add_argument("--source", choices=["google", "linkedin", "both"], default="both", help="Data source to extract from (google, linkedin, or both)")
    parser.add_argument("--query", type=str, default="Data Engineer", help="Job search query (default: 'Data Engineer')")
    parser.add_argument("--location", type=str, default="United States", help="Job location (default: 'United States')")
    parser.add_argument("--output", choices=["csv", "sqlite", "both"], default="both", help="Output format: csv, sqlite, or both (default: both)")
    
    args = parser.parse_args()
    
    main(args=args)