import time
import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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

            symbol = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            price = cols[3].get_text(strip=True)

            results.append({
                "symbol": symbol,
                "name": name,
                "price": price
            })

            print(f'{results=}')

        return results