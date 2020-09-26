import scraper
from scraper import find_jobs_from
import time
website = "Indeed"
jobs = ["developer", "python", "programmer", "data science"] 
location = "paignton"
saved_cols = ['titles', 'companies', 'salary', 'links', 'date_listed']
#todo: append each result to 1 spreadsheet instead of multiple created each run
#iterate over each job
for job in jobs:
    filename = website + "_" + job + "_" + time.strftime("%d") + "_" + time.strftime("%m") + "_" + time.strftime("%Y") + ".xlsx" #indeed_developer_dd_mm_yyyy.xlsx
    find_jobs_from(website, job, location, saved_cols, filename)