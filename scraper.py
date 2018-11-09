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
time.sleep(4)
browser.execute_script("window.scrollTo(0, 10000);")
time.sleep(4)

soup = bs(browser.html, 'html.parser')

browser.quit()

table = soup.find_all('table', class_='resortList')[0].find('tbody')
resort_rows = table.find_all('tr')
for i in range(len(resort_rows)):
	# resort_name = resort_rows[i].find('a').text
	# print('--------------------------------------------------------------------------------------------')
	# print('Row {}'.format(i))
	cells = resort_rows[i].find_all('td')
	for cell in cells:
		# resort name
		if 'resort' in cell['class']:
			resort_name = cell.find('a').text
		# new snow
		if 'openstate' in cell['class']:
			div = cell.find('div')
			if 'background-color: rgb(28, 148, 0);' in div['style']:
				open_status = True
			else:
				open_status = False
		if 'nsnow' in cell['class']:
			inches = cell.find_all('b')
			inches_24_hr = inches[0].text
			inches_72_hr = inches[1].text
		if 'open_lifts' in cell['class']:
			open_lifts = cell.text
		if 'trails' in cell['class']:
			open_trails = cell.text
	# print(resort_name)

