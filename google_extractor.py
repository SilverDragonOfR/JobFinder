import os
import requests

def extract_google_jobs(query, location):
    
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": serpapi_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Jobs API: {e}")
        return []
    
    data = response.json()
    job_results = data.get("jobs_results", [])
    jobs = []
    
    for job in job_results:
        extracted_job = {
            "Job Title": job.get("title", None),
            "Company": job.get("company_name", None),
            "Location": job.get("location", None),
            "Job Description": job.get("description", None),
            "Job URL": (job.get("apply_options", [])[0] if job.get("apply_options", []) else {}).get("link", None),
            "Job Posting Time": job.get("detected_extensions", {}).get("posted_at", None)
        }
        jobs.append(extracted_job)
    
    return jobs