from celery.schedules import crontab
from celery import Celery
from job_pipeline_repeat import run_job_pipeline

app = Celery(
    "job_pipeline",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Scheduled job that runs daily
@app.task
def scheduled_job_run():
    from job_pipeline import run_job_pipeline
    print("Running scheduled job...")
    run_job_pipeline()

app.conf.beat_schedule = {
    'run-every-day': {
        'task': 'tasks.scheduled_job_run',
        'schedule': crontab(hour=0, minute=0),
    },
}