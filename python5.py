import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch product details
def main(URL, data):
    # specifying user agent
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })
    
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    
    # Retrieving product title
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string.strip().replace(',', '') if title else "NA"
    except AttributeError:
        title_value = "NA"
    
    # Retrieving price
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '') if soup.find("span", attrs={'id': 'priceblock_ourprice'}) else "NA"
    except AttributeError:
        price = "NA"
    
    # Retrieving product rating
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '') if soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}) else "NA"
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '') if soup.find("span", attrs={'class': 'a-icon-alt'}) else "NA"
        except:
            rating = "NA"
    
    # Retrieving review count
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '') if soup.find("span", attrs={'id': 'acrCustomerReviewText'}) else "NA"
    except AttributeError:
        review_count = "NA"
    
    # Retrieving availability status
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '') if available else "NA"
    except AttributeError:
        available = "NA"

    # Printing the details
    print("Product Title:", title_value)
    print("Product Price:", price)
    print("Product Rating:", rating)
    print("Review Count:", review_count)
    print("Availability:", available)
    
    # Append the data to the list
    data.append({
        'Title': title_value,
        'Price': price,
        'Rating': rating,
        'Review Count': review_count,
        'Availability': available
    })

# Main function to process multiple URLs
def process_urls():
    
    # List to store the product data
    product_data = []

    # Reading URLs from file
    with open("product_data.xlsx", "r") as file:
        # Iterating over the URLs
        for link in file.readlines():
            main(link.strip(), product_data)
    
    # Converting the data to a DataFrame
    df = pd.DataFrame(product_data)
    
    # Saving to Excel (you can also change the path and filename as needed)
    df.to_excel("product_data.xlsx", index=False, engine='openpyxl')

if __name__ == "__main__":
    process_urls(
    
    )
