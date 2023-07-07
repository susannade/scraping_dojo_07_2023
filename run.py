import sys
from driver_builder import DriverBuilder
from quotes import ScrapingProcess


if __name__ == "__main__":
    env_file_path = '.env'
    driver_builder = DriverBuilder()
    scraping_process = ScrapingProcess(env_file_path, driver_builder)
    scraping_process.run()
    sys.exit(0)
