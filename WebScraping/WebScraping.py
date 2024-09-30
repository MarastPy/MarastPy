import requests
from bs4 import BeautifulSoup
import pandas as pd


targetfile = 'files/WebUrlTester.xlsx'
url = 'https://www.konicaminolta.cz/'

try:
    reqs = requests.get(url)
    reqs.raise_for_status()  # Check if the request was successful
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    exit()

soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and isinstance(href, str) and ((href.startswith('http')) and not (href.endswith('html'))):
        print(href)
        urls.append(href)

with pd.ExcelWriter(targetfile) as writer:
    pd.DataFrame(urls, columns=['URL']).to_excel(writer, sheet_name='Tester', index=False)