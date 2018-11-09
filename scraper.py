import bs4 as bs
import requests

url = 'https://www.onthesnow.com/epic-pass/skireport.html'

html = requests.get(url).text

table = html.find('table', class_='resortList')

print(table)