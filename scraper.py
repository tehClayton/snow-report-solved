from bs4 import BeautifulSoup as bs
from splinter import Browser
import urllib.request
import time

# fn to initialize browser object
def init_browser():
	# @NOTE: Replace the path with your actual path to the chromedriver
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)

# url to scrape
url = 'https://www.onthesnow.com/epic-pass/skireport.html'

# instantiate browser
browser = init_browser()
# go to page
browser.visit(url)
# wait for dynamic elements to load
time.sleep(4)
# page uses lazy loading, so force a scroll action to load more resorts
browser.execute_script("window.scrollTo(0, 10000);")
# wait for page to load
time.sleep(4)

# instantiate soup object
soup = bs(browser.html, 'html.parser')

# we're done with our browser
browser.quit()

# extract relevant table
table = soup.find_all('table', class_='resortList')[0].find('tbody')
# extract rows for each resort
resort_rows = table.find_all('tr')
for i in range(len(resort_rows)):
	# added some print statements to help us extract useful info prior to building dictionaries
	# print('--------------------------------------------------------------------------------------------')
	# print('Row {}'.format(i))
	cells = resort_rows[i].find_all('td')
	for cell in cells:
		# resort name
		if 'resort' in cell['class']:
			resort_name = cell.find('a').text
		# open status
		if 'openstate' in cell['class']:
			div = cell.find('div')
			# the background color of the circle seems to be our best bet
			# for identifying open status
			if 'background-color: rgb(28, 148, 0);' in div['style']:
				open_status = True
			else:
				open_status = False
		# new snow
		if 'nsnow' in cell['class']:
			inches = cell.find_all('b')
			inches_24_hr = inches[0].text
			inches_72_hr = inches[1].text
		# open lifts
		if 'open_lifts' in cell['class']:
			open_lifts = cell.text
		# open trails
		if 'trails' in cell['class']:
			open_trails = cell.text
	# print(resort_name)

