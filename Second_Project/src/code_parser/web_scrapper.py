import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebScraper:
    """
    A class to scrape Regions/Countries from a specific web page.

    Attributes:
        url (str): The URL of the web page to scrape.

    Methods:
        scrape(): Scrapes regions/countries information and returns it as a DataFrame.
    """

    def __init__(self, url):
        self.url = url

    def scrape(self):
        # Send a request to the World Bank website
        response = requests.get(self.url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all country elements
        countries = soup.find_all("li", class_="tt-suggestion")

        # Extract and store the country data
        data = []
        for country in countries:
            anchor = country.find("a", class_="country-name")
            if anchor:
                name = anchor.text.strip()
                url = anchor['href']
                data.append({"name": name, "url": url})

        # Convert to DataFrame
        return pd.DataFrame(data)


