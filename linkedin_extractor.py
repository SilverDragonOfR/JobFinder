import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def extract_linkedin_jobs(query, location, max_possible=10, within_24hrs=False):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    
    driver = webdriver.Chrome(options=options)
    
    base_url = "https://www.linkedin.com/jobs/search/"
    if within_24hrs:
        # params = f"?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r86400"
        params = f"?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r172800&f_E=1"
    else:
        params = f"?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    url = base_url + params
    driver.get(url)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/main/section[2]/button")))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            time.sleep(random.choice(range(3, 7)))
        except Exception as e:
            print(e)
            break
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        if within_24hrs:
            job_listings_timing = soup.find_all("time", class_="job-search-card__listdate--new")
        else:
            job_listings_timing = soup.find_all("time", class_="job-search-card__listdate")
            
            
        job_listings_timing = [job.get_text(strip=True).lower() for job in job_listings_timing if job]
        
        if within_24hrs:
            job_listings_timing = [timing for timing in job_listings_timing if (("hour" in timing) or ("min" in timing) or ("sec" in timing))]
            
        if len(job_listings_timing) >= max_possible:
            break

    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

    try:
        for job in job_listings:
            if len(jobs) >= max_possible:
                break
            
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            job_location = job.find("span", class_="job-search-card__location").text.strip()
            apply_link = job.find("a", class_="base-card__full-link")["href"]
            posting_time = job.find("time").get_text(strip=True)
            
            if within_24hrs:
                posting_time_lower = posting_time.lower()
                if ("hour" not in posting_time_lower) and ("min" not in posting_time_lower) and ("sec" not in posting_time_lower):
                    continue
            
            driver.get(apply_link)
            
            time.sleep(random.choice(range(5, 11)))
            
            try:
                company_soup = BeautifulSoup(driver.page_source, "html.parser")
                job_description = company_soup.find("div", class_="description__text description__text--rich").text.strip()
                company_link_tag = company_soup.find("a", class_="sign-up-modal__company_webiste")
                
                # If company_link_tag is None, then this means it is "Easy Apply" so linkedin link is the actual ATS link
                if company_link_tag:
                    company_link = company_link_tag["href"]
                    driver.get(company_link)
                    time.sleep(5)
                    actual_ats_link = driver.current_url
                else:
                    actual_ats_link = apply_link
            except Exception as e:
                job_description = None
                actual_ats_link = apply_link
                print(f"Error occurred while retrieving job description and url: {e}")
            
            jobs.append({
                "Job Title": job_title,
                "Company": job_company,
                "Location": job_location,
                "Job Description": job_description,
                "Job URL": actual_ats_link,
                "Job Posting Time": posting_time
            })
            
    except Exception as e:
        print(f"An error occurred while scraping jobs: {str(e)}")
        return jobs

    driver.quit()
    return jobs