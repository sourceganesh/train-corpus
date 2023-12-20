import requests
from bs4 import BeautifulSoup
import re

def get_job_descriptions(job_title, location, num_pages=5):
    base_url = f'https://www.indeed.com/jobs?q={job_title}&l={location}'
    job_descriptions = []

    for page in range(1, num_pages + 1):
        url = f'{base_url}&start={page * 10}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for job_card in soup.find_all('div', class_='jobsearch-SerpJobCard'):
            job_link = job_card.find('a', class_='jobtitle')
            if job_link:
                job_url = f'https://www.indeed.com{job_link["href"]}'
                job_description = get_job_description(job_url)
                job_descriptions.append(job_description)

    return job_descriptions

def get_job_description(job_url):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description_section = soup.find('div', class_='jobsearch-jobDescriptionText')
    if description_section:
        description_text = description_section.get_text(separator='\n')
        # Remove non-alphanumeric characters and extra whitespaces
        clean_description = re.sub(r'[^a-zA-Z0-9\s]', '', description_text)
        return clean_description.lower()

    return None

if _name_ == "_main_":
    job_title = 'software+developer'
    location = 'your_location'
    num_pages = 5

    corpus = get_job_descriptions(job_title, location, num_pages)

    # Save the generated corpus to a file
    with open('software_development_corpus.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(corpus))
