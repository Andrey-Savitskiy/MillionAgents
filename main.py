import re
import csv
import time

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import logger, URL, TOWNS, option


def price_edit(price: str) -> str:
    delete_whitespace = re.sub(' ', '', price)
    return re.sub(',', '.', delete_whitespace)[:-2]


def load_page(driver: WebDriver, page_counter: int, town: str) -> None:
    driver.get(URL + str(page_counter))

    if town == 'spb' and page_counter == 1:
        region = driver.find_element(by=By.XPATH, value='//*[@id="app-container"]/div[2]/header/div[2]/div/div[1]/ul/li[1]')
        region.click()

        spb = driver.find_element(by=By.XPATH, value='/html/body/div[9]/div/div[2]/section/div/ul/li[1]/ul/li[1]/span')
        spb.click()
        time.sleep(3)


def get_product_list(driver: WebDriver) -> list:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    products_list = soup.find_all('div', class_='n_2')
    return products_list


def product_info(product: Tag, town: str) -> None:
    product_url = product.find('a')['href']
    # print(product_url)
    product_id = product_url.split('/')[-2]
    # print(product_id)
    product_name = product.find('p', class_='Kj').text
    # print(product_name)

    try:
        product_price = price_edit(product.find('span', class_='Kw').text)
        product_promo_price = price_edit(product.find('p', class_='Ku').text)
    except AttributeError:
        product_price = price_edit(product.find('p', class_='Ku').text)
        product_promo_price = '---'

    # print(f'{product_price} : {product_promo_price}')
    # print()

    with open('result.csv', mode='a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter = ',', lineterminator='\n')
        file_writer.writerow([product_id, product_name, product_price,
                              TOWNS[town], product_promo_price, product_url])


def parser(driver: WebDriver, town: str) -> int:
    page_counter = 1
    load_page(driver, page_counter, town)
    products_list = get_product_list(driver)

    while len(products_list) > 0:
        for product in products_list:
            try:
                product_info(product, town)
            except AttributeError:
                return 0

        print(f'{page_counter}: {len(products_list)}')

        page_counter += 1
        load_page(driver, page_counter, town)
        products_list = get_product_list(driver)

    return 0


@logger.catch()
def main():
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
    driver.implicitly_wait(10)
    try:
        for town_key in TOWNS.keys():
            parser(driver, town_key)
            print(f'End of {town_key}\n')

        # time.sleep(60)
    finally:
        driver.close()


if __name__ == '__main__':
    main()
