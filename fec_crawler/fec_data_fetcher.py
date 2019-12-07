import requests
import os
import time

class FECDataFetcher(object):
  BASE_URL = 'https://api.open.fec.gov/v1'
  API_KEY = os.getenv("FEC_API_KEY")
  PER_PAGE = 100

  def __init__(self, *args, pagination=None, params=None, paged=False):
    self._endpoint = '/'.join([self.BASE_URL] + list(args))
    self._paged = paged
    self._params = params or {}
    self.data = []
    self._len = 0
    self.pagination = pagination or {}
    self.head = 0
    self._at_end = False
    self.get_data()

  @property
  def params(self):
    p = {
        'api_key': self.API_KEY,
        'per_page': self.PER_PAGE,
        }
    p.update(self._params)
    p.update(self.pagination)
    return p

  def __len__(self):
    return self._len

  def __iter__(self):
    return self

  def __next__(self):
    if self.head >= len(self.data):
      self.get_data()
      self.head = 0
    if self.data:
      ret = self.data[self.head]
      self.head += 1
      return ret
    raise StopIteration

  def get_data(self, retry=0):
    if self._at_end:
      self.data = None
      return

    rsp = requests.get(self._endpoint, self.params)

    if not rsp.ok:
      if retry > 10:
        msg = "[{}] Failed to get data: {}".format(rsp.status_code, rsp.text)
        raise ValueError(msg)
      time.sleep(2 ** retry)
      return self.get_data(retry + 1)

    rsp_data = rsp.json()
    self.data = rsp_data['results']
    self._len = rsp_data['pagination']['count']
    if self._paged:
      self.pagination['page'] = rsp_data['pagination']['page'] + 1
    else:
      pg = rsp_data['pagination']['last_indexes']
      if pg:
        self.pagination.update(pg)
      else:
        self._at_end = True
