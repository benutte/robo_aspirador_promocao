import requests
from bs4 import BeautifulSoup
import time


def fetch_page():
        url = "https://www.amazon.com.br/aspirador-X6-navega%C3%A7%C3%A3o-Aspirador-autom%C3%A1tica/dp/B0DH1CRRPX?th=1"
        response = requests.get(url)
        return response.text


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('span', class_="a-size-large product-title-word-break").get_text()
    price: list = soup.find_all('span', class_="a-price-whole")
    old_price: int = int(price[0].get_text().replace('.', '').replace(',', ''))

    return {
        'product_name': product_name,
        'old_price': old_price
    }

      
if __name__ == "__main__":
    while True:
         page_content = fetch_page()
         produto_inf = parse_page(page_content)
         print(produto_inf)
         time.sleep(10)
