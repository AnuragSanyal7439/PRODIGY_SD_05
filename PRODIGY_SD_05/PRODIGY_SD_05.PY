import requests
from bs4 import BeautifulSoup
import csv


URL = "https://www.awwwards.com/websites/e-commerce/" 


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_product_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to fetch the webpage:", response.status_code)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    
    
    product_containers = soup.find_all("div", class_="product-item") 
    
    products = []
    for product in product_containers:
        try:
            
            name = product.find("h2", class_="product-title").text.strip()
            
            price = product.find("span", class_="product-price").text.strip()
            
            rating = product.find("div", class_="product-rating").text.strip()

            
            products.append({
                "Name": name,
                "Price": price,
                "Rating": rating
            })
        except AttributeError:
            
            continue
    return products


def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    print("Scraping product data...")
    product_data = get_product_data(URL)

    if product_data:
        output_file = "products.csv"
        save_to_csv(product_data, output_file)
        print(f"Data successfully saved to '{output_file}'.")
    else:
        print("No data was found.")
