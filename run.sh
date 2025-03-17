celery -A tasks beat --loglevel=info
python job_pipeline.py --source both --query "Data Engineer" --time "24hrs" --location "United States" --output csv