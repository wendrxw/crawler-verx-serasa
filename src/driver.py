import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from decouple import config
from .logger import setup_logger


class Handler:
    def __init__(self, filters: str = None):
        self.filters = filters
        self.logger = setup_logger()

        self.logger.info("Iniciando crawler sem filtros" if not self.filters else f"Iniciando crawler filtrando pela região: {self.filters}")

        self.now = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        self.url = config("URL")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(
            options=self.options
        )
        self.driver.get(self.url)
        self.filter_by_region()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table tbody tr")
            )
        )

    def filter_by_region(self):
        if not self.filters:
            return
        
        WebDriverWait(
            self.driver, 
            10
        ).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(., 'Filters')]"
            ))
        ).click()

        clear_all_btn = WebDriverWait(
            self.driver, 
            5
        ).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[.//text()[contains(., 'Clear All')]]"
            ))
        )
        self.driver.execute_script(
            "arguments[0].click();",
            clear_all_btn
        )
        time.sleep(0.5)
        
        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Region')]"
            ))
        ).click()

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//span[text()='{self.filters}']"
            ))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[.//text()[contains(., 'Apply')]]"
            ))
        ).click()

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
            self.logger.info(f"Coletando dados da pagina {page}")

            data = self.extract()
            results.extend(data)

            if not self.pagination():
                break

            page += 1

        return results

    def load_as_csv(self, data: list):
        self.logger.info("Iniciando gravação dos dados para CSV")
        df = pd.DataFrame(data)
        df = df[["symbol", "name", "price"]]
        df.to_csv(f"stocks_{self.now}.csv", index=False)
        self.logger.info("Gravação dos dados para CSV finalizada")