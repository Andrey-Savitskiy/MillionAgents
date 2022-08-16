import time
import csv
import requests
from bs4 import BeautifulSoup as bs
from loguru import logger
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

logger.add('logs/debug.log', level="WARNING", rotation="50 MB", compression='zip',
           enqueue=True, backtrace=True, diagnose=True)


URL = "https://www.detmir.ru/catalog/index/name/zdorovyj_perekus_pp/page/"


def product_info(product: WebElement):
    product_url = product.get_attribute('href')
    print(product_url)
    product_id = product_url.split('/')[-2]
    print(product_id)
    product_name = product.find_element(By.CLASS_NAME, 'Kj').text
    print(product_name)
    print()
    time.sleep(0.2)


def parser(driver: WebDriver, town: str):
    driver.get(URL)
    a = driver.page_source
    products_list = driver.find_elements(By.CLASS_NAME, 'Kf')

    for product in products_list:
        try:
            product_info(product)
        except StaleElementReferenceException:
            driver.get(URL)
            product_info(product)
            continue
        #
        # product_price = product.find_element(By.CLASS_NAME, 'Uz').text
        # if product_price:
        #     product_promo_price = product.find_element(By.CLASS_NAME, 'Ux').text
        # else:
        #     product_price = product.find_element(By.CLASS_NAME, 'Ux').text
        #     product_promo_price = '---'






@logger.catch()
def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        # region = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[2]/header/div[2]/div/div[1]/ul/li[1]/div/div/div[1]/div/span')
        # region.click()
        parser(driver, 'Moscow')



        time.sleep(60)
    finally:
        driver.close()


if __name__ == '__main__':
    main()
