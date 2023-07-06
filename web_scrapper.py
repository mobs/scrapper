import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Selenium WebDriver
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# list to store various details of the products
product_url=[]
product_name = []
product_price = []
product_rating = []
product_reviews = []

# Setting the page number to be scraped to 25 as it was asked to scrape atleat 20 pages
num_pages = 25

# Iterating over each page for scraping sequentially
for page in range(1, num_pages + 1):
    driver.get(f'https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}')

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')))
    except TimeoutException:
        print(f"Timeout occurred while waiting for the search results on page {page}")
        continue

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Searching for the results
    search_results = soup.find_all('div', {'data-component-type': 's-search-result'})

    # iterating over each of the search result and extracting the relevant information 
    for result in search_results:

        # Extracting Product URL
        url = result.find('a', class_='a-link-normal s-no-outline')['href']
        url = 'https://www.amazon.in' + url

        # Extracting Product Name
        name = result.find('span', class_='a-size-medium a-color-base a-text-normal').text.strip()

        # Extracting Product Price
        pro_price = result.find('span', class_='a-offscreen')
        price = pro_price.text.strip() if pro_price else 'Price not available'

        # Extracting Rating
        rating = result.find('span', {'class': 'a-icon-alt'})
        
        if rating:
            rating = rating.text.split()[0]
        else:
            rating = 'Not available'


        # Extracting Number of reviews
        reviews = result.find('span', {'class': 'a-size-base s-underline-text'})
        if reviews:
            reviews = reviews.text.strip()
        else:
            reviews = 'Not available'
        
        product_url.append(url)
        product_name.append(name)
        product_price.append(price)
        product_rating.append(rating)
        product_reviews.append(reviews)


# saving all the details using pandas to the required format of .csv
data = pd.DataFrame({'Product URL':product_url,
    'Product Name': product_name,
    'Product Price': product_price,
    'Rating': product_rating,
    'Number of Reviews': product_reviews
})

data.to_csv('products.csv', index=False, encoding='utf-8-sig')
