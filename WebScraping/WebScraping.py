import requests
from bs4 import BeautifulSoup

# Specify the target URL
url = 'https://www.lego.com/cs-cz/categories/sales-and-deals'

# Fetch the page content
response = requests.get(url)

if response.status_code == 200:
    # Save the raw HTML to a file
    with open("html_scraping.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Create an empty list to store product names, prices, and availability
    products = []

    # Find all product containers (adjust based on actual structure of the site)
    product_containers = soup.find_all("h3", class_="ProductLeaf_titleRow__KqWbB")  # This matches the product titles

    # Iterate through each product container
    for product in product_containers:
        # Find the product name
        name_element = product.find("a", class_="ProductLeaf_title__1UhfJ")
        product_name = name_element.text.strip() if name_element else "N/A"

        # Find the price (traverse the parent div to get price associated with the product)
        price_div = product.find_next("div", class_="ProductLeaf_priceRow__RUx3P")
        price_element = price_div.find("span", {"data-test": "product-leaf-discounted-price"}) if price_div else None
        product_price = price_element.text.strip() if price_element else "N/A"

        # Check for availability (like "Coming Soon" message)
        availability_element = product.find_next("a", {"data-test": "product-leaf-cta-coming-soon"})
        availability_status = "Coming Soon" if availability_element else "Available"

        # Add the product name, price, and availability to the list
        products.append((product_name, product_price, availability_status))

    # Print or store the product names, prices, and availability
    print("Product Names, Prices, and Availability:")
    for product in products:
        print(f"Product: {product[0]} - Price: {product[1]} - Status: {product[2]}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


'''

for link in soup.find_all('div', class_='pricevalue'):    
    href = link.get('href')
    if href and isinstance(href, str) and ((href.startswith('http')) and not (href.endswith('html'))):
        #print(href)
        urls.append(href)

with pd.ExcelWriter(targetfile) as writer:
    pd.DataFrame(urls, columns=['URL']).to_excel(writer, sheet_name='Tester', index=False)

'''

