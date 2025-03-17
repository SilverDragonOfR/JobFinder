# JobFinder: Automated Job Posting Extraction and Storage

## Overview

JobFinder is a Python-based application designed to automate the extraction, transformation, and storage of job postings from online platforms. This tool streamlines the process of collecting job market data, specifically targeting roles such as "Data Engineer." It utilizes web scraping techniques and APIs to gather data from Google Jobs and LinkedIn, processing and storing this information in structured formats for analysis and tracking.

## Functionality

JobFinder automates the following key processes:

1.  **Extraction:**
    *   **Google Jobs Extractor:** Leverages the SerpAPI ([serpapi.com](https://serpapi.com/)) to retrieve job postings from Google Jobs programmatically. It queries the SerpAPI with specified job titles and locations, extracting data from the API responses.
    *   **LinkedIn Extractor:** Employs Selenium and BeautifulSoup4 for web scraping job postings directly from LinkedIn. This involves browser automation to navigate search results and extract job details, including job descriptions from individual job pages.

2.  **Transformation:**
    *   **Data Cleaning and Standardization:** The `data_transformer.py` script processes the extracted data to ensure consistency and quality. This includes:
        *   Standardizing text formatting (whitespace normalization, case consistency).
        *   Handling missing values and encoding issues.
        *   Deduplicating job postings to ensure data uniqueness.

3.  **Storage:**
    *   **CSV and SQLite Output:** The cleaned job data is stored in two formats for versatility:
        *   CSV (`jobs_output.csv`): Data is appended to a CSV file, with duplicate entries removed.
        *   SQLite (`jobs_output.sqlite`): Data is stored in an SQLite database (`job_postings` table), also with duplicate removal. Timestamps are recorded for each data entry.

## Technical Approach

The codebase is structured into modular Python scripts, each responsible for a specific stage of the data pipeline:

*   **`google_extractor.py`**: Implements job extraction from Google Jobs using SerpAPI.
    *   **Method:** API requests to SerpAPI, parsing JSON responses.
    *   **Tool:** `requests` library for HTTP requests.

*   **`linkedin_extractor.py`**: Implements job extraction from LinkedIn.
    *   **Method:** Web scraping using browser automation and HTML parsing.
    *   **Tools:** `selenium` for browser automation, `BeautifulSoup4` for HTML parsing, `chromedriver` for Chrome browser control.

*   **`data_transformer.py`**: Cleans and transforms extracted job data.
    *   **Method:** Dataframe manipulation and cleaning operations.
    *   **Tool:** `pandas` library for data manipulation, `re` for regular expressions.

*   **`storage.py`**: Handles data storage in CSV and SQLite formats.
    *   **Method:** Data export and database operations.
    *   **Tools:** `pandas` for CSV export, `sqlite3` for SQLite database interaction.

*   **`job_pipeline.py`**: Orchestrates the end-to-end job data pipeline for single runs.
    *   **Method:** Command-line argument parsing and sequential execution of extraction, transformation, and storage steps.
    *   **Tool:** `argparse` for command-line argument parsing, `dotenv` for environment variable loading.

*   **`job_pipeline_repeat.py`**: Designed for scheduled, repeated job data extraction.
    *   **Method:** Hardcoded parameters for automated daily runs of the data pipeline.

*   **`tasks.py`**: Configures scheduled task execution using Celery.
    *   **Method:** Defines Celery tasks and schedules for automated daily runs.
    *   **Tools:** `celery`, `celery.schedules`, `redis` (broker and backend).

## Setup and Installation

### Prerequisites

*   **Python 3.x:**  Install Python 3.x from [python.org](https://www.python.org/).
*   **pip:** Python package installer (typically included with Python).
*   **Google Chrome:** Install Google Chrome from [google.com/chrome/](https://www.google.com/chrome/) (required for LinkedIn scraping).
*   **ChromeDriver:** Download the ChromeDriver compatible with your Chrome version from [chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads). Ensure ChromeDriver is added to your system's `PATH` environment variable.
*   **SerpAPI Key:** Obtain a SerpAPI API key from [serpapi.com](https://serpapi.com/).
*   **Redis (for scheduled runs):** Install Redis from [redis.io/download/](https://redis.io/download/) if daily scheduled runs are required.

### Installation Steps

1.  **Clone Repository (if applicable):**

    ```bash
    git clone [repository_url]
    cd JobFinder
    ```

2.  **Create Virtual Environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate.bat  # Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure SerpAPI Key:**
    *   Create a `.env` file in the project root.
    *   Add your SerpAPI key to `.env` as: `SERPAPI_KEY=YOUR_SERPAPI_API_KEY_HERE`

## Execution

JobFinder supports both one-time and scheduled daily executions.

### One-Time Execution

Execute `job_pipeline.py` for a single data extraction run with customizable parameters.

```bash
python job_pipeline.py --source <source> --query "<job_query>" --location "<location>" --output <output_format>
```

### Daily Scheduled Execution

For daily automated runs, configure and use Celery with `tasks.py` and `job_pipeline_repeat.py`.

1.  **Start Redis Server:** Ensure Redis server is running. Command may vary based on your system (e.g., `redis-server`).

2.  **Start Celery Beat Scheduler:** Open a terminal in the project directory and run:

    ```bash
    celery -A tasks beat --loglevel=info
    ```

    This initiates the Celery Beat scheduler, which will execute `job_pipeline_repeat.py` daily at midnight (as configured in `tasks.py`). Keep this process running for scheduled executions.

3. **Stopping Scheduled Runs:** Terminate the Celery Beat process (e.g., `Ctrl+C`).


## New Job Pipeline Changes

This update introduces several enhancements to the job scraping pipeline:

- **Converted Links to Direct ATS Links:**  
  The script now retrieves the actual ATS link by clicking the "company website" button instead of using the default LinkedIn apply URL. This ensures that candidates are directed straight to the employer's application page.

- **CSV Output Option:**  
  The pipeline also exports job data to a CSV file. A sample output file (`jobs_output.csv`) is provided.

- **Time Filter Option:**  
  A new command-line argument `--time` has been added to filter job postings based on recency. When you specify `--time "24hrs"`, the script returns only those postings that indicate they were published within the last 24 hours (e.g., "4 hours ago", "17 hours ago", "23 hours ago"). The default value is `any`, which retrieves postings regardless of time.

- **Location Filter Option:**  
  The job search now also accepts a location filter. For example, using `--location "United States"` will limit the job search to that specific location.

- **Internal Option to control the number of job posting extracted from Google Jobs & Linkedin:**  
  The internal parameter `max_possible` in both google_extractor.py and linkedin_extractor.py to control the maximum number of jobs which will be extracted from each.

### New Test Argument

```bash
python job_pipeline.py --source both --query "Data Engineer" --time "24hrs" --location "United States" --output "csv"
```
