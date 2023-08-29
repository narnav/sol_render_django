from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from datetime import datetime

def display(msg):
    print("message: ", msg)

scheduler = BlockingScheduler()
# scheduler.add_job(display, 'date', run_date = datetime(2023, 8, 24,23, 48, 0 ), args=["Job1"])
scheduler.add_job(display, 'cron', hour = 23, minute = 54, args=["Job1"])

scheduler.start()
