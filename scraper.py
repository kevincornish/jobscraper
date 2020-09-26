import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

def find_jobs_from(website, job_title, location, saved_cols, filename):    
    #potentially add more websites later on
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, saved_cols)
       
    save_to_excel(jobs_list, filename)
 
    print('{} new jobs from {}, saved as {}.'.format(num_listings, website, filename))

def save_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)

def load_indeed_jobs_div(job_title, location):
    #lets pass in the varibles from main.py to the search query
    #fromage:last= last visit
    #sort:date = newest posted first
    getVars = {'q' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars)) #urlencode the vars so we don't break the search
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol") #find resultsCol and search from inside here
    return job_soup

def extract_job_information_indeed(job_soup, saved_cols):
    #each result is stored inside div class=jobsearch-SerpJobCard so lets grab each one
    job_elems = job_soup.find_all('div', class_='jobsearch-SerpJobCard')
     
    cols = []
    extracted_info = []
    
    #make the columns optional in excel 

    if 'titles' in saved_cols:
        titles = []
        cols.append('Job Titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)          
    
    if 'companies' in saved_cols:
        companies = []
        cols.append('Companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)
        
    if 'salary' in saved_cols:
        salary = []
        cols.append('Salary')
        for job_elem in job_elems:
            salary.append(extract_salary_indeed(job_elem))
        extracted_info.append(salary)
    
    if 'links' in saved_cols:
        links = []
        cols.append('Link')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)
    
    if 'date_listed' in saved_cols:
        dates = []
        cols.append('Date Listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
    
    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings

def extract_job_title_indeed(job_elem):
    #find the h2 with title class and extract the text
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    #some titles were returning 'new' appended to the end so lets strip that out
    title = title.replace('new', '')
    return title
    
def extract_salary_indeed(job_elem):
    #try to find the span with class salary and extract the text, some don't include salarys so we can make an exception and return salary not stated
    try:
        salary_elem = job_elem.find('span', class_='salaryText')
        salary = salary_elem.text.strip()
    except AttributeError:
        salary = "Salary not stated"
    return salary

def extract_company_indeed(job_elem):
    #find the a span with class company and grab just the text from it.
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    #find the a href link, append it to base url.
    link = job_elem.find('a')['href']
    link = 'https://www.indeed.co.uk' + link
    return link

def extract_date_indeed(job_elem):
    #find the span with class date and grab just the text from it.
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date