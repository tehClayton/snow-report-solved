from bs4 import BeautifulSoup as bs
from splinter import Browser
import urllib.request
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

url = 'https://www.onthesnow.com/epic-pass/skireport.html'

browser = init_browser()
browser.visit(url)
time.sleep(2)


soup = bs(browser.html, 'html.parser')

table = soup.find_all('table')

browser.quit()

print(table)