from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from os import getcwd
from selenium.webdriver import DesiredCapabilities
from random import randrange

option = Options()
prefs = {
    "translate_whitelists": {
        "es": "en",
        "ru": "en",
        "id": "en",
        "pt": "en",
        "ko": "en",
        "fr": "en",
        "ar": "en",
        "it": "en",
        "nl": "en",
        "th": "en",
        "tr": "en",
        "vi": "en",
        "he": "en",
        "ja": "en",
        "pl": "en"
    },
    "translate": {"enabled": "true"},
    "profile.default_content_setting_values.notifications": 2
}
option.add_experimental_option("prefs", prefs)
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument("--lang=en")
option.add_argument("--headless")
"""option.set_preference('dom.webnotifications.enabled', False)"""
option.add_argument("--window-size=1920,1080")


req_proxy = RequestProxy()
proxies = req_proxy.get_proxy_list()
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']

"""profile.set_preference('devtools.jsonview.enabled', False)
profile.set_preference('intl.accept_languages', 'ru, en')
profile.set_preference("translate", "true")"""


def page_content():
    PROXY = proxies[randrange(len(proxies))].get_address()
    DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "Manual"
    }
    DesiredCapabilities.CHROME["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(executable_path=f"{getcwd()}\chromedriver.exe", options=option)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agents[randrange(2)]})
    driver.switch_to.window(driver.current_window_handle)
    return driver

