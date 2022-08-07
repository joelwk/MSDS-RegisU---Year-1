from bs4 import BeautifulSoup
import pandas as pd
import requests
#https://www.youtube.com/watch?v=PPcgtx0sI2E&list=WL&index=2

def extract(job,location_city,location_state,page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q={job}&l={location_city}+{location_state}&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_ = 'cardOutline')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_ = 'companyName').text.strip()
        location = item.find('div', class_ = 'companyLocation').text.strip()
        try:
            salary = item.find('span', class_ = 'metadata salary-snippet-container').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return


def get_data(job,location_city,location_state,max_pages):
    import pandas as pd
    
    job = job
    location_city = location_city
    location_state = location_state

    page = 0
    
    joblist = []
    for i in range(0,max_pages,10):
        c = extract(job,location_city,location_state,i)
        transform(c)
    
    df = pd.DataFrame(joblist)

