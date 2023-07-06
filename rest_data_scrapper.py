import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Read the existing data from the CSV file using pandas library
try:
    existing_data = pd.read_csv('products.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame()


# Extracting the URLs from the existing data
urls = existing_data['Product URL']

# Iterating over the URLs and updating the data
for index,url in enumerate(urls[:200]):
    driver.get(url)  # Visiting the URL using Selenium

    # Waiting for the page to load completely
    driver.implicitly_wait(10)

    # Extracting the desired information from the webpage
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extracting ASIN
    asin = soup.find('input', {'name': 'ASIN'})['value']

    # Extracting product description
    parent = soup.find_all('li', class_='a-spacing-mini')
    description = ""
    for desc in parent:
        description = description + ' ' + desc.find_next('span',class_='a-list-item').text.strip()

    # Extracting manufacturer name
    manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    manufacturer = manufacturer.replace("Visit the","Brand:")
    manufacturer = manufacturer.replace("Store","")

    # Updating the corresponding row in the DataFrame with the new information
    mask = (existing_data['Product URL'] == url)
    existing_data.loc[mask, 'ASIN'] = asin
    existing_data.loc[mask, 'Description'] = description
    existing_data.loc[mask, 'Manufacturer'] = manufacturer

# If the DataFrame is empty, creating new columns for the data
if existing_data.empty:
    existing_data['ASIN'] = ''
    existing_data['Description'] = ''
    existing_data['Manufacturer'] = ''

# Writing the updated data back to the CSV file
existing_data.to_csv('products.csv', index=False, encoding='utf-8-sig')
