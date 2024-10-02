import requests
from bs4 import BeautifulSoup
import pandas as pd

def request_url(url):
    try:
        reqs = requests.get(url)
        reqs.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(reqs.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        exit()

targetfile = 'WebUrlTester.xlsx'

#url = 'https://www.alza.cz/hracky/lego/vyprodej-akce-sleva/18851136-e0'
url = 'https://www.lego.com/cs-cz/categories/new-sets-and-products'


soup = request_url(url)


with open('html_scraping.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())


#print(soup)
print('------------------------------------------------------------')


urls = []

soup = soup.find('div', class_='pricevalue')

print(soup)



'''

for link in soup.find_all('div', class_='pricevalue'):    
    href = link.get('href')
    if href and isinstance(href, str) and ((href.startswith('http')) and not (href.endswith('html'))):
        #print(href)
        urls.append(href)

with pd.ExcelWriter(targetfile) as writer:
    pd.DataFrame(urls, columns=['URL']).to_excel(writer, sheet_name='Tester', index=False)

'''