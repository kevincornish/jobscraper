# Job Scraper

Quick and easy job scraper in python, currently only scraping indeed.co.uk

# Installation
## Install requirements
```bash
pip install -r requirements.txt
```

## Settings
### main.py
```python
website = "Indeed"
jobs = ["developer", "python", "programmer", "data science"] 
location = "paignton"
saved_cols = ['titles', 'companies', 'salary', 'links', 'date_listed']
```

# Running Scraper
```bash
python main.py
```
