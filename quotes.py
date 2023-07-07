import os
import json
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui


class Quote:
    def __init__(self, text, by, tags):
        self.text = text
        self.by = by
        self.tags = tags

    def process_quote_elements(self):
        self.text = self.text.replace('\u201c', '').replace('\u201d', '')
        self.by = self.by.replace('by ', '')
        self.tags = self.tags.replace('Tags: ', '').split(' ')


class ScrapingProcess:
    def __init__(self, env_file_path, driver_builder, timeout=60):
        load_dotenv(dotenv_path=env_file_path)
        self.proxy = os.getenv("PROXY")
        self.input_url = os.getenv("INPUT_URL")
        self.output_file = os.getenv("OUTPUT_FILE")
        self.driver_builder = driver_builder
        self.timeout = timeout
        self.wait = None
        self.quotes_list = []

    def process_quote(self, quote_elem):
        keys = ["text", "by", "tags"]
        elem_list = quote_elem.text.split('\n')
        dictionary = dict(zip(keys, elem_list))
        quote = Quote(dictionary.get("text"), dictionary.get("by"), dictionary.get("tags"))
        quote.process_quote_elements()
        self.quotes_list.append(quote)

    def scrape_quotes(self):
        # Setting proxy
        # self.driver_builder.set_proxy(proxy=self.proxy)
        driver = self.driver_builder.get_driver()
        self.wait = ui.WebDriverWait(driver, self.timeout)
        print(f'Scraping page {self.input_url}')

        while True:
            driver.get(self.input_url)
            self.wait.until(lambda d: d.find_elements(By.CLASS_NAME, 'quote'))

            for quote in driver.find_elements(By.CLASS_NAME, 'quote'):
                self.process_quote(quote)

            next_page_elem = driver.find_elements(By.XPATH, '//a[contains(@href,"page") and contains(text(),"Next")]')
            if next_page_elem:
                next_page_url = next_page_elem[0].get_attribute('href')
                print(f'Scraping page {next_page_url}')
                self.input_url = next_page_url
            else:
                print(f'No more pages to scrap...')
                break

        driver.quit()

    def save_quotes(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for item in self.quotes_list:
                f.write(json.dumps(item.__dict__, ensure_ascii=False) + "\n")
        print(f"Data {self.output_file} saved")

    def run(self):
        print("Processing...")
        self.scrape_quotes()
        self.save_quotes()
