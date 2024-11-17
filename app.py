import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3



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

def create_connection(db_name='robo_aspirador.db'):
     """Cria uma conexao com o banco de dados SQLite."""
     conn = sqlite3.connect(db_name)
     return conn

def setup_database(conn):
     """Cria a tabela de preços se ela não existir"""
     cursor = conn.cursor()
     cursor.execute('''
                    CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT,
                    old_price INTEGER,
                    timestamp TEXT
                    )
                ''')
     conn.commit()

def save_to_database(conn, produto_info):
     new_row = pd.DataFrame([produto_info])
     #df = pd.concat([df, new_row], ignore_index=True)
     new_row.to_sql('prices', conn, if_exists='append', index=False)

if __name__ == "__main__":

    conn = create_connection()
    setup_database(conn)
    #df = pd.DataFrame()

    while True:
         page_content = fetch_page()
         produto_info = parse_page(page_content)
         save_to_database(conn, produto_info)
         print("Dados Salvo: ", produto_info)
         time.sleep(10)
