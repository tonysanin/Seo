from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import time
import random

ENTER = u'\ue007'

def CreateBrowser(proxy, head=False, window=False, ua=False):
    if proxy:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.ssl_proxy = proxy
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)

    # Set random user agent
    opts = Options()
    if ua:
        ua = UserAgent()
        agent = ua.chrome
        opts.add_argument("user-agent=" + agent)
    if not head:
        opts.add_argument("--headless")
    if window:
        opts.add_argument("--window-size=" + window)
    else:
        opts.add_argument("--window-size=%s" % "1920,1080")

    if proxy:
        _browser = webdriver.Chrome(options=opts, desired_capabilities=capabilities)
    else:
        _browser = webdriver.Chrome(options=opts)
    return _browser


def ClickOnElementByXpath(_browser, _xpath):
    action = ActionChains(_browser)
    action.move_to_element(_browser.find_element_by_xpath(_xpath)).perform()
    time.sleep(random.uniform(0.1, 0.3))
    action.click().perform()

def OpenURL(_browser, _url):
    _browser.get(_url)


def FindInGoogle(browser, query, site_to_search):   # Функция ищет в гугле сайт и переходит на него
    page = 0
    url = "https://google.com"
    browser.get(url)    # Переходим по ссылке
    time.sleep(random.uniform(1, 3))    # Имитируем ожидание

    try:
        enter_field = browser.find_element_by_xpath("/html/body/div/div[4]/form/div[2]/div[1]/div[1]/div/div[2]/input")
    except:
        print("Captcha or bad useragent")
        return False
    for s in query: # Пишем запрос, имитируя задержку
        enter_field.send_keys(s)
        time.sleep(random.uniform(0.1, 1))

    # Рандомим ещё один ввод. Enter/наведение мыши
    #method = random.randint(0, 1)
    method = 2
    if method == 1:
        action = ActionChains(browser)
        action.move_to_element(browser.find_element_by_xpath("/html/body/div/div[4]/form/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]")).perform()
        time.sleep(random.uniform(0.1, 0.3))
        action.click().perform()
    else:
        enter_field.send_keys(ENTER)


    while True:
        time.sleep(random.uniform(2, 4))
        try:
            results = browser.find_elements_by_css_selector(".a, cite, cite a:link, cite a:visited, .cite, .cite:link, .bc a:link")
        except:
            print("Captcha or bad useragent")
            return False
        if (len(results) == 0):
            print("Captcha or bad useragent")
            return False
        for result in results:
            print(result.text)
            if result.text.find(site_to_search) != -1:
                time.sleep(0.5)
                browser.execute_script("window.scrollTo(0, window.scrollY + " + str(random.randint(0, 100)) + ")")
                time.sleep(2)
                result.click()
                return 1
        action = ActionChains(browser)
        some_elements = browser.find_elements_by_css_selector("#res h3, #extrares h3")
        action.move_to_element(some_elements[random.randint(0, len(some_elements) - 1)]).perform()
        time.sleep(0.25)
        browser.execute_script("window.scrollTo(0, window.scrollY + 1000)")
        time.sleep(random.uniform(3, 5))
        try:
            browser.execute_script("pnnext.click()")
        except:
            print("No more pages. Can't find your site")
            return False
        page += 1
        if (page == 15):
            print("15 pages. Can't find your site!")
            return False
