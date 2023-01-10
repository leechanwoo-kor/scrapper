from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  
  browser = webdriver.Chrome(options=options)  
  browser.get(f"https://kr.indeed.com/jobs?q={keyword}")
  
  html = browser.page_source
  
  soup = BeautifulSoup(html, "html.parser")
  pagination = soup.find("nav", role="navigation")
  if pagination == None:
    return 1
  pages = pagination.find_all("div", recursive=False)
  count = len(pages)
  if count >= 5:
    return 5
  else:
    return count

def extract_indeed_jobs(keyword):
  results = []
  
  pages = get_page_count(keyword)
  print("Fonud", pages, "pages")
  for page in range(pages):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(options=options)  
    
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page*10}"

    print("Requesting", final_url)
    browser.get(final_url)
    
    html = browser.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all('li', recursive=False)
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        job_data = {
          'link': f"https://kr.indeed.com{link}",
          'company': company.string.replace(","," "),
          'location': location.string.replace(","," "),
          'position': title.replace(","," "),
        }
        results.append(job_data)
  return results