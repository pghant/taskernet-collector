# Methods to interact with Google Play

from bs4 import BeautifulSoup
import requests

def get_app_name(package):
  url = f'https://play.google.com/store/apps/details?id={package}'
  res = requests.get(url)
  soup = BeautifulSoup(res.text, features='html.parser')
  app_name = soup.select_one('h1[itemprop="name"] span').text
  return app_name
