import time
import argparse
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from decouple import config


class Handler:
    def __init__(self):
        self.now = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        self.url = config("URL")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            options=self.options
        )
        self.driver.get(self.url)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table tbody tr")
            )
        )

    def extract(self):
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

        return results
    
    def pagination(self):
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'button[data-testid="next-page-button"]'
                ))
            )
            
            if not btn.is_enabled():
                return False
            
            first_cell_text = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "table tbody tr td"
            )[0].text
            
            self.driver.execute_script(
                "arguments[0].click();", 
                btn
            )

            WebDriverWait(self.driver, 15).until(
                lambda d: d.find_elements(
                    By.CSS_SELECTOR, 
                    "table tbody tr td"
                )[0].text != first_cell_text
            )

            return True
        except Exception:
            return False
        
    def run(self):
        results = []
        page = 1

        while True:
            print(f'{page=}')

            data = self.extract()
            results.extend(data)

            if not self.pagination():
                break

            page += 1

        return results

    
    def load_as_csv(self, data: list):
        df = pd.DataFrame(data)
        df = df[["symbol", "name", "price"]]
        df.to_csv(f"stocks_{self.now}.csv", index=False)