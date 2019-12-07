'''
.. module:: errors
   :synopsis: Iterator factories that wrap some FEC API endpoints

.. moduleauthor:: Andrew Milligan <andrew.i.milligan@gmail.com>

'''


class Error(Exception):
    '''
    Base error class for other more specific error classes
    '''
    pass


class FecApiError(Error):
    '''
    Raised when there is a problem encountered with the FEC API (e.g., when an
    invalid request is made or when the API rate limit is exceeded after all
    retries are exhausted)
    '''
    pass
