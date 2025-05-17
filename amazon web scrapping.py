from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"}).text.strip()
        return title
    except AttributeError:
        return None

def get_price(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price-whole"}).text.strip()
        return price
    except AttributeError:
        return None

def get_rating(soup):
    try:
        rating = soup.find("span", attrs={"class": "a-icon-alt"}).text.strip()
        return rating
    except AttributeError:
        return None

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={"id": "acrCustomerReviewText"}).text.strip()
        return review_count
    except AttributeError:
        return None

def get_availability(soup):
    try:
        availability = soup.find("div", attrs={"id": "availability"}).find("span").text.strip()
        return availability
    except AttributeError:
        return "Not Available"

# Function to scrape multiple pages
def scrape_pages(num_pages):
    HEADERS = {'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'}
    base_url = "https://www.amazon.in/s?k=realme&crid=MZHTAMNI4D9Q&sprefix=realm%2Caps%2C354&ref=nb_sb_noss_2&page="

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    for page_num in range(1, num_pages+1):
        URL = base_url + str(page_num)
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
        links_list = []
        for link in links:
            links_list.append(link.get('href'))

        for link in links_list:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))

    # Convert to DataFrame
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(f"Scraped data from {num_pages} pages and saved to 'amazon_data.csv'.")

# Main block to ask user for the number of pages to scrape
if __name__ == '__main__':
    try:
        num_pages = int(input("Enter the number of pages you want to scrape: "))
        scrape_pages(num_pages)  # Scrapes the specified number of pages
    except ValueError:
        print("Please enter a valid number.")
