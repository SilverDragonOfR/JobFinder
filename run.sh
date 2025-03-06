celery -A tasks beat --loglevel=info
python job_pipeline.py --source both --query "Data Engineer" --location "United States" --output both