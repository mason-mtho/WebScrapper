from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.edge.service import Service
import boto3
from datetime import datetime
import time
import os

proxy = "http://o365proxy.africa.nedcor.net:80"

# Set the path to your Edge WebDriver 
edge_driver_path = "C:\\Users\\NB437080\\Downloads\\edgedriver_win64\\msedgedriver.exe"
service = Service(executable_path=edge_driver_path)

# Initialize Edge WebDriver 
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

# def scrape_simple():

#     proxy = "http://o365proxy.africa.nedcor.net:80"
#     # Set the path to your Edge WebDriver 
#     edge_driver_path = "C:\\Users\\NB437080\\Downloads\\edgedriver_win64\\msedgedriver.exe"

#     # Initialize Edge WebDriver 
#     options = webdriver.EdgeOptions() 
#     driver = webdriver.Edge(options=options)
#     # Open a website 
#     #driver.get("https://www.farfetch.com/za/sets/new-in-this-week-eu-men.aspx?page=1/")
#     driver.get('http://quotes.toscrape.com/js/')

#     # Wait for JavaScript to load
#     time.sleep(5)

#     # Find all quotes on the page 
#     quotes_elements = driver.find_elements(By.CLASS_NAME, 'quote')

#     os.environ['http_proxy'] = proxy
#     os.environ['https_proxy'] = proxy
#     # Connect to DynamoDB 
#     dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
#     table = dynamodb.Table('QuotesTable')
#     os.environ['http_proxy'] = ''
#     os.environ['https_proxy'] = ''

#     # Extract and store data 
#     for quote_element in quotes_elements: 
#         text = quote_element.find_element(By.CLASS_NAME, 'text').text 
#         author = quote_element.find_element(By.CLASS_NAME, 'author').text 
#         tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, 'tag')]
#         # Create a unique Quote ID 
#         quote_id = str(hash(text))

#         # Save data to DynamoDB 
#         table.put_item( 
#             Item={ 
                
#                 'Quote_id': quote_id,
#                 'Author_name': author, 
#                 'Quote text': text, 
#                 'Tags': ", ".join(tags),
#                 'Scraped_at': str(datetime.now())})

#     print("Quotes have been scraped and stored in DynamoDB.")
#     # Print page title 
#     print(driver.title)

#     # Call to function, passing last page number to scrape
#     # Close the browser
#     driver.quit()

# scrape_simple()
    
def dynamic_scrape(page):
    for i in range(1,(page + 1)):
        # Open a website 
        driver.get("https://www.farfetch.com/za/sets/new-in-this-week-eu-men.aspx?page=" +  str(i))

        # Wait for JavaScript to load
        time.sleep(15)

        # full stop is for spaces and spaces are for nested elements
        # css.selector

        # Find all clothes on the page 
        clothing_elements = driver.find_elements(By.CLASS_NAME, 'ltr-2u1m5k')
        #clothing_elements = driver.find_elements(By.TAG_NAME, "ul")

        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        # Connect to DynamoDB 
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
        table = dynamodb.Table('ClothingTable')
        os.environ['http_proxy'] = ''
        os.environ['https_proxy'] = ''

        # Extract and store data 
        for clothing_element in clothing_elements: 
            brand = clothing_element.find_element(By.CLASS_NAME, 'ltr-10idii7-Body-BodyBold').text 
            description = clothing_element.find_element(By.CLASS_NAME, 'ltr-4y8w0i-Body').text 
            price = clothing_element.find_element(By.CLASS_NAME, 'ltr-1dazc2-Body.e9qb0mc0').text
            
            # Create a unique Clothing ID 
            clothing_id = str(hash(brand + description))

            print(clothing_id)

            # Save data to DynamoDB 
            table.put_item( 
                Item={ 
                    'Clothing_id': clothing_id,
                    'Brand': brand, 
                    'Description': description, 
                    'Price': price,
                    'Scraped_at': str(datetime.now()) 
                    })
        
    print("Clothes have been scraped and stored in DynamoDB.")
    # Print page title 
    print(driver.title)

# Call to function, passing with last page number to scrape
dynamic_scrape(1)

# Close the browser
driver.quit()

