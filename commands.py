from BrowserUtils import *
from random import randint
import time

def loadProxy():
    proxies = [line.rstrip('\n') for line in open('proxy.txt')]
    return proxies

def createBrowser(params, proxies):
    resolution = params.split("\"")[1].replace("\"", '')
    params = params.split(',')
    print(params[0])
    if params[0] == "randomProxy":
        proxy = proxies[randint(0, len(proxies)-1)]
        print(proxy)
    if params[0] == "None":
        proxy = False

    window = False
    if params[1].find("True") != -1:
        window = True
    if params[1].find("False") != -1:
        window = False

    ua = True
    if params[len(params) - 1].find("True") != -1:
        ua = True
    if params[len(params) - 1].find("False") != -1:
        ua = False
    return CreateBrowser(proxy, window, resolution, ua)

def findInGoogle(browser, params):
    params = params.split("\",")
    query = params[0].replace('"', '')
    site = params[1].replace('"', '').lstrip()
    if not FindInGoogle(browser, query, site):
        browser.close()
        return False
    return True

def wait(_time):
    time.sleep(_time)

def scroll(browser, range):
    browser.execute_script("window.scrollTo(0, window.scrollY + " + str(range) + ")")

def clickOnElement(browser, xpath):
    ClickOnElementByXpath(browser, xpath)

def openUrl(browser, url):
    OpenURL(browser, url)
