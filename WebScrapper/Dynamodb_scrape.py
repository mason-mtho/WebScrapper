import requests 
from bs4 import BeautifulSoup 
import boto3 
from datetime import datetime
# Initialize DynamoDB resource 
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', verify=False) 
# Update with your region 
table = dynamodb.Table('QuotesTable') # Use your table name
# Function to scrape quotes from the website 
def scrape_quotes(): 
    url = 'http://quotes.toscrape.com/' 
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, 'html.parser')
    # Loop through each quote on the page
    for quote in soup.find_all('div', class_='quote'): 
        text = quote.find('span', class_='text').text 
        author = quote.find('small', class_='author').text 
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        # Create a unique Quote ID (hash of the quote text)  
        quote_id = str(hash(text))
        # Save the quote data to DynamoDB 
        table.put_item( 
            Item={ 
            'Quote_id': quote_id, 
            'Author_name': author, 
            'Quote_text': text, 
            'Tags': ", ".join(tags), 
            'Scraped_at': str(datetime.now()) # Timestamp of when scraped 
            } 
        )
    print("Quotes have been scraped and stored in DynamoDB.")
# Run the function 
scrape_quotes()