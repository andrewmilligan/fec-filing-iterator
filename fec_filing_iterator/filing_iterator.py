import requests
import time
from errors import FecApiError


class FilingIterator(object):
    '''
    This class encapsulates the logic of interacting with the FEC API and
    iterating through the paged results that are returned in order to present
    the full set of results as a single, lazily evaluated, iterable stream.
    '''

    BASE_URL = 'https://api.open.fec.gov/v1'

    def __init__(
        self,
        *args,
        api_key=None,
        params=None,
        pagination=None,
        per_page=100,
        paged=False
    ):
        self._api_key = api_key
        self._endpoint = '/'.join([self.BASE_URL] + list(args))
        self._paged = paged
        self._params = params or {}
        self._len = 0
        self._pagination = pagination or {}
        self._per_page = per_page
        self._head = 0
        self._at_end = False
        self.data = self.get_data()

    @property
    def params(self):
        p = {
            'api_key': self._api_key,
            'per_page': self._per_page,
        }
        p.update(self._params)
        p.update(self._pagination)
        return p

    def __len__(self):
        return self._len

    def __iter__(self):
        return self

    def __next__(self):
        if self._head >= len(self.data):
            self.data = self.get_data()
            self._head = 0
        if not self.data:
            raise StopIteration
        ret = self.data[self._head]
        self._head += 1
        return ret

    def fetch_json(self, url, params={}):
        retry = 0
        while retry < 10:
            rsp = requests.get(url, params)
            if rsp.ok:
                return rsp.json()

            if rsp.status_code != 429:
                break

            time.sleep(2 ** retry)
            retry += 1

        if rsp.status_code == 429:
            msg = 'FEC API rate limit exceeded and retries exhausted'
            raise FecApiError(msg)

        try:
            msg = rsp.json()['message']
        except Exception:
            msg = rsp.text

        raise FecApiError(msg)

    def get_data(self, retry=0):
        if self._at_end:
            return None

        rsp_data = self.fetch_json(self._endpoint, self.params)
        self._len = rsp_data['pagination']['count']

        if self._paged:
            self._pagination['page'] = rsp_data['pagination']['page'] + 1
        else:
            pg = rsp_data['pagination']['last_indexes']
            if pg:
                self._pagination.update(pg)
            else:
                self._at_end = True
        return rsp_data['results']
