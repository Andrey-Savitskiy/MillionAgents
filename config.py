from loguru import logger
from selenium.webdriver.chrome.options import Options

logger.add('logs/debug.log', level="WARNING", rotation="50 MB", compression='zip',
           enqueue=True, backtrace=True, diagnose=True)


URL = "https://www.detmir.ru/catalog/index/name/zdorovyj_perekus_pp/page/"

TOWNS = {
    'mos': 'Москва и Московская область',
    'spb': 'Санкт-Петербург и Ленинградская область'
}

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
