import time
import argparse
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from decouple import config


class Handler:
    def __init__(self):
        self.url = config("URL")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            options=self.options
        )
        self.driver.get(self.url)

    def extract_data(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        rows = soup.select("table tbody tr")
        results = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            symbol = cols[1].get_text(strip=True)
            name = cols[2].get_text(strip=True)
            price = cols[4].get_text(strip=True)

            results.append({
                "symbol": symbol,
                "name": name,
                "price": price
            })

            print(f'{results=}')

            self.load_as_csv(results)

        return results
    
    def load_as_csv(self, data: list):
        df = pd.DataFrame(data)
        df = df[["symbol", "name", "price"]]
        df.to_csv("stocks.csv", index=False)