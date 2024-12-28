import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3
from telegram import Bot
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Configuração do bot do Telegram

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token = TOKEN)


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

def get_max_price(conn):
     cursor = conn.cursor()
     cursor.execute("SELECT old_price, timestamp FROM prices ORDER BY timestamp ASC LIMIT 1")
     result =cursor.fetchone()
     if result and result[0] is not None:
        return result[0], result[1]
     return None, None

async def send_telegram_message(text):
     await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():

    conn = create_connection()
    setup_database(conn)
    max_price, max_price_timestamp = get_max_price(conn)
    try:
                             
        while True:
            page_content = fetch_page()
            produto_info = parse_page(page_content)
            current_price = produto_info['old_price']
                
            # Comparação de preços
            if max_price is None or current_price > max_price:
                message = (
                    f"Novo preço maior detectado: {current_price}\n"
                    f"Anterior maior preço: {max_price if max_price else 'N/A'} em {max_price_timestamp if max_price_timestamp else 'N/A'}"
                )
                print(message)
                await send_telegram_message(message)
                max_price = current_price
                max_price_timestamp = produto_info['timestamp']
            else:
                message = (
                    f"O maior preço registrado é {max_price}\n"
                    f"Preço atual: {current_price} em {max_price_timestamp}"
                )
                print(message)
                await send_telegram_message(message)

            save_to_database(conn, produto_info)
            #print("Dados salvos no banco:", produto_info)
            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("Parando a execução...")
    finally:
        conn.close()

# Executa o loop assíncrono
asyncio.run(main())
