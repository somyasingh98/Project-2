import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
class MakeupAPIHandler:
    """
    A class for handling requests to the Makeup API and analyzing the retrieved data.

    Methods
    -------
    fetch_data():
        Makes a GET request to the Makeup API and returns the data as a DataFrame.
    
    analyze_data(dataframe):
        Analyzes the data in the provided DataFrame, offering insights like average prices, popular brands, etc.
    """

    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            data = response.json()

            print(f"Retrieved {len(data)} products from the Makeup API.")

            # Define the fields you want to extract
            fields = ['id', 'brand', 'name', 'price', 'rating', 'product_type', 
                    'price_sign', 'currency', 'image_link', 'product_link', 
                    'website_link', 'description', 'category', 'tag_list', 
                    'created_at', 'updated_at', 'product_api_url', 
                    'api_featured_image', 'product_colors']

            # Extracting and storing only the specified fields in the DataFrame
            extracted_data = [{field: product.get(field, None) for field in fields} for product in data]
            dataframe = pd.DataFrame(extracted_data)

            return dataframe
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def analyze_data(self, dataframe):
        if dataframe is not None and not dataframe.empty:

            # Clean the 'price' column by removing non-numeric characters and converting to float
            # Clean the 'price' column by removing non-numeric characters and converting to float
            dataframe['price'] = dataframe['price'].str.extract('(\d+\.\d+)').astype(float)


            # Basic EDA
            print("Basic Exploratory Data Analysis:")
            # Number of products
            num_products = len(dataframe)
            print(f"Number of Products: {num_products}")

            # Number of unique brands
            num_brands = dataframe['brand'].nunique()
            print(f"Number of Unique Brands: {num_brands}")

            # Number of unique product types
            num_product_types = dataframe['product_type'].nunique()
            print(f"Number of Unique Product Types: {num_product_types}")

            # Average rating
            avg_rating = dataframe['rating'].mean()
            print(f"Average Rating: {avg_rating:.2f}")

            # Price statistics
            print("Price Statistics:")
            price_stats = dataframe['price'].describe()
            print(price_stats)

            # Price Comparison
            print("\nPrice Comparison:")
            # Group by brand and calculate the average price for each brand
            brand_avg_price = dataframe.groupby('brand')['price'].mean()
            # Sort the brands by average price in descending order
            brand_avg_price = brand_avg_price.sort_values(ascending=False)
            print(brand_avg_price)

            # Products with the highest prices
            highest_prices = dataframe.nlargest(5, 'price')
            print("Products with the Highest Prices:")
            print(highest_prices[['brand', 'name', 'price']])

            # Products with the lowest prices
            lowest_prices = dataframe.nsmallest(5, 'price')
            print("Products with the Lowest Prices:")
            print(lowest_prices[['brand', 'name', 'price']])

            # Price Distribution Histogram
            plt.figure(figsize=(10, 6))
            sns.histplot(dataframe['price'], bins=20, kde=True)
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.title('Price Distribution')
            plt.grid(True)
            plt.show()

            # Brand Comparison Bar Plot
            plt.figure(figsize=(12, 8))
            sns.barplot(x='brand', y='price', data=dataframe, ci=None)
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('Brand')
            plt.ylabel('Average Price')
            plt.title('Average Price Comparison by Brand')
            plt.grid(axis='y')
            plt.tight_layout()
            plt.show()
                        # Further analyses can be added based on requirements

        else:
            print("No data to analyze.")

    


