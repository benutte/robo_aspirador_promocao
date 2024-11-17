import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def fetch_page():
        url = "https://www.amazon.com.br/aspirador-X6-navega%C3%A7%C3%A3o-Aspirador-autom%C3%A1tica/dp/B0DH1CRRPX?th=1"
        response = requests.get(url)
        return response.text


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('span', class_="a-size-large product-title-word-break").get_text()
    price: list = soup.find_all('span', class_="a-price-whole")
    old_price: int = int(price[0].get_text().replace('.', '').replace(',', ''))

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'product_name': product_name,
        'old_price': old_price,
        'timestamp': timestamp
    }

def save_to_dataframe(product_inf, df):
     new_row = pd.DataFrame([product_inf])
     df = pd.concat([df, new_row], ignore_index=True)
     return df
if __name__ == "__main__":
    df = pd.DataFrame()

    while True:
         page_content = fetch_page()
         produto_inf = parse_page(page_content)
         df = save_to_dataframe(produto_inf, df)
         print(df)
         time.sleep(10)
