import requests

def fetch_page(url):
        response = requests.get(url)
        return response.text

if __name__ == "__main__":
    url = "https://www.amazon.com.br/aspirador-X6-navega%C3%A7%C3%A3o-Aspirador-autom%C3%A1tica/dp/B0DH1CRRPX?th=1"
    page_content = fetch_page(url)
    print(page_content)
