# Methods to interact with TaskerNet API

import requests

from utils import parse_link

def get_share_data(share_link):
  user, share_id = parse_link(share_link)
  if user == None:
    raise InvalidShareUrlError(api_url)

  api_url = f'https://taskernet.com/_ah/api/datashare/v1/shares/{user}/{share_id}'
  resp = requests.get(api_url)

  if resp.status_code == 404:
    raise ShareDoesNotExistError(api_url)
  elif resp.status_code != 200:
    raise GenericError(api_url)

  return resp.json()

class ApiError(Exception):
  """ Base Exception for API calls """
  pass

class ShareDoesNotExistError(ApiError):
  def __init__(self, message):
    self.message = message

class InvalidShareUrlError(ApiError):
  def __init__(self, message):
    self.message = message

class GenericError(ApiError):
  def __init__(self, message):
    self.message = message
