import requests
import pandas as pd
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import gzip
import io
import logging
import os
class ZillowXMLParser:
    def __init__(self, base_url):
        """
        Initialize the ZillowXMLParser with a specific base URL.
        """
        self.base_url = base_url

    def get_robots_txt(self):
        """
        Get the contents of the robots.txt file from Zillow's base URL.

        Returns:
            str: The contents of the robots.txt file.
        """
        try:
            response = requests.get(f"{self.base_url}/robots.txt")
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            logging.error(f"HTTP error while getting robots.txt: {e}")
            return ''
        except Exception as e:
            logging.error(f"An error occurred while getting robots.txt: {e}")
            return ''

    def find_sitemaps(self, robots_txt):
        """
        Extract sitemap URLs from Zillow's robots.txt content.

        Parameters:
            robots_txt (str): The contents of the robots.txt file.

        Returns:
            list: A list of sitemap URLs.
        """
        sitemaps = []
        for line in robots_txt.splitlines():
            if line.startswith('Sitemap:'):
                sitemaps.append(line.split(': ')[1])
        return sitemaps

    def scrape_content(self, url):
        """
        Scrape the content from a given URL on Zillow.

        Parameters:
            url (str): The URL to scrape content from.

        Returns:
            str: The scraped content as text.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            content_soup = BeautifulSoup(response.text, 'html.parser')
            if content_soup and hasattr(content_soup, 'text'):
                return content_soup.text
            else:
                return ''  # Return an empty string if no content found
        except HTTPError as e:
            logging.error(f"HTTP error while scraping content: {e}")
            return ''
        except Exception as e:
            logging.error(f"An error occurred while scraping content: {e}")
            return ''


    # def parse_sitemap(self, sitemap_url, output_dir):
    #     """
    #     Parse an XML sitemap or sitemap index from Zillow and extract information. Handles both gzipped and regular XML files.

    #     Parameters:
    #             sitemap_url (str): The URL of the XML sitemap or sitemap index to parse.
    #             output_dir (str): The directory to save the scraped content.

    #     Returns:
    #             pandas.DataFrame: A DataFrame containing URL, Last Modified, and Content columns.
    #         """
    #     try:
    #         response = requests.get(sitemap_url)
    #         response.raise_for_status()

    #         # Try parsing as gzipped file first
    #         try:
    #             with gzip.open(io.BytesIO(response.content), 'rt') as f:
    #                 tree = ET.parse(f)
    #                 is_gzipped = True  # Indicate that the content is gzipped
    #         except gzip.BadGzipFile:
    #             # If not gzipped, parse as regular XML
    #             tree = ET.fromstring(response.content)
    #             is_gzipped = False  # Indicate that the content is not gzipped

    #         scraped_data = []
            
    #         # Check if it's a sitemap index
    #         if tree.tag.endswith('sitemapindex'):
    #             for sitemap in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
    #                 sitemap_loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    #                 # Recursively parse the referenced sitemap
    #                 df = self.parse_sitemap(sitemap_loc, output_dir)
    #                 if not df.empty:
    #                     scraped_data.extend(df.to_dict('records'))
    #         else:
    #             # It's an individual sitemap, parse it
    #             for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    #                 loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    #                 lastmod_element = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
    #                 lastmod = lastmod_element.text if lastmod_element is not None else 'Not available'
    #                 content = self.scrape_content(loc)

    #                 scraped_data.append({'URL': loc, 'Last Modified': lastmod, 'Content': content})

    #                 # Save the gzipped content if it was gzipped
    #                 if is_gzipped:
    #                     content_filename = os.path.join(output_dir, f"{os.path.basename(loc)}.gz")
    #                     with open(content_filename, 'wb') as content_file:
    #                         content_file.write(response.content)

    #             return pd.DataFrame(scraped_data)
    #     except HTTPError as e:
    #         print(f"HTTP error while parsing sitemap: {e}")
    #         return pd.DataFrame()
    #     except Exception as e:
    #         print(f"An error occurred while parsing sitemap: {e}")
    #         return pd.DataFrame()


    def parse_sitemap(self, sitemap_url):
        """
        Parse an XML sitemap from Zillow and extract information. Handles both gzipped and regular XML files.

        Parameters:
            sitemap_url (str): The URL of the XML sitemap to parse.

        Returns:
            pandas.DataFrame: A DataFrame containing URL, Last Modified, and Content columns.
        """
        try:
            response = requests.get(sitemap_url)
            response.raise_for_status()

            # Try parsing as gzipped file first
            try:
                with gzip.open(io.BytesIO(response.content), 'rt') as f:
                    tree = ET.parse(f)
                    is_gzipped = True  # Indicate that the content is gzipped
            except gzip.BadGzipFile:
                # If not gzipped, parse as regular XML
                tree = ET.fromstring(response.content)
                is_gzipped = False  # Indicate that the content is not gzipped

            scraped_data = []
            for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                lastmod_element = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
                lastmod = lastmod_element.text if lastmod_element is not None else 'Not available'
                content = self.scrape_content(loc)

                scraped_data.append({'URL': loc, 'Last Modified': lastmod, 'Content': content})

            return pd.DataFrame(scraped_data)
        except HTTPError as e:
            print(f"HTTP error while parsing sitemap: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"An error occurred while parsing sitemap: {e}")
            return pd.DataFrame()
