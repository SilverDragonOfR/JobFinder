import time
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def extract_linkedin_jobs(query, location):
    # We'll load 2 pages
    pages = 2
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(options=options)
    
    base_url = "https://www.linkedin.com/jobs/search/"
    params = f"?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    url = base_url + params
    
    driver.get(url)

    # Scroll and click "Show more" multiple times
    for i in range(pages):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/main/section[2]/button")
                )
            )
            element.click()
        except Exception:
            print("Show more button not found, retrying...")

        time.sleep(random.choice(list(range(3, 7))))

    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all(
        "div",
        class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
    )

    # Collect details from each job card
    try:
        for job in job_listings:
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            job_company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            job_location = job.find("span", class_="job-search-card__location").text.strip()
            apply_link = job.find("a", class_="base-card__full-link")["href"]
            posting_time = job.find("time").get_text(strip=True)

            driver.get(apply_link)

            time.sleep(random.choice(list(range(5, 11))))

            try:
                description_soup = BeautifulSoup(driver.page_source, "html.parser")
                job_description = description_soup.find("div", class_="description__text description__text--rich").text.strip()

            except AttributeError:
                job_description = None
                print("AttributeError occurred while retrieving job description.")

            jobs.append(
                {
                    "Job Title": job_title,
                    "Company": job_company,
                    "Location": job_location,
                    "Job Description": job_description,
                    "Job URL": apply_link,
                    "Job Posting Time": posting_time
                }
            )

    except Exception as e:
        print(f"An error occurred while scraping jobs: {str(e)}")
        return jobs

    driver.quit()
    return jobs
