import pandas as pd
import sqlite3
from datetime import datetime

def store_to_csv(df, csv_file="jobs_output.csv"):
    # Add timestamp to each row
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        existing_df = pd.read_csv(csv_file)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        unique_columns = [col for col in df.columns if col not in ["Timestamp", "Job Posting Time"]]
        combined_df.drop_duplicates(subset=unique_columns, keep="first", inplace=True)
    except FileNotFoundError:
        combined_df = df
    
    combined_df.to_csv(csv_file, index=False)
    print(f"Data successfully appended to {csv_file} (duplicates removed).")

def store_to_sqlite(df, sqlite_file="jobs_output.sqlite", table_name="job_postings"):
    # Add timestamp to each row
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(sqlite_file)
    existing_df = pd.read_sql(f"SELECT * FROM {table_name}", conn) if table_name in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() else pd.DataFrame()
    
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        unique_columns = [col for col in df.columns if col not in ["Timestamp", "Job Posting Time"]]
        combined_df.drop_duplicates(subset=unique_columns, keep="first", inplace=True)
    else:
        combined_df = df
    
    combined_df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data successfully stored in {sqlite_file}, table: {table_name} (duplicates removed).")
