import pytest # noqa
from fec_filing_iterator import errors


def test_error():
    '''
    Base Error class can be caught as an Exception
    '''
    try:
        raise errors.Error("test error")
    except Exception as e:
        assert str(e) == "test error"


def test_fec_api_error():
    '''
    FecApiError can be caught as a base Error
    '''
    try:
        raise errors.FecApiError("test error")
    except errors.Error as e:
        assert str(e) == "test error"
