import os
import requests

def extract_google_jobs(query, location, max_possible=10, within_24hrs=False):
    
    serpapi_key = os.getenv("SERPAPI_KEY")
    url = "https://serpapi.com/search"
    
    jobs = []
    next_page_token = None
    
    while len(jobs) < max_possible:
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": serpapi_key,
            "chips": "date_posted:today"
        }
        if next_page_token:
            params["next_page_token"] = next_page_token
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Google Jobs API: {e}")
            break
        
        data = response.json()
        job_results = data.get("jobs_results", [])
        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token", "")
        
        if not job_results:
            break
        
        for job in job_results:
            posting_time = job.get("detected_extensions", {}).get("posted_at", None)
            
            if within_24hrs:
                if not posting_time:
                    continue
                posting_time_lower = posting_time.lower()
                if ("hour" not in posting_time_lower) and ("min" not in posting_time_lower) and ("sec" not in posting_time_lower):
                    continue
            
            extracted_job = {
                "Job Title": job.get("title", None),
                "Company": job.get("company_name", None),
                "Location": job.get("location", None),
                "Job Description": job.get("description", None),
                "Job URL": (job.get("apply_options", [])[0] if job.get("apply_options", []) else {}).get("link", None),
                "Job Posting Time": posting_time
            }
            jobs.append(extracted_job)
            
            if len(jobs) >= max_possible:
                break
        
    return jobs