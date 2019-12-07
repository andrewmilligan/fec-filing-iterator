import pytest
import mock
from fec_filing_iterator import filing_iterator, errors


@mock.patch('requests.get')
def test_filing_iterator_indexes(mock_get):
    # Given
    mock_get.return_value.json.side_effect = [
        {
            'results': range(100),
            'pagination': {
                'count': 110,
                'last_indexes': {
                    'foo': 'bar',
                },
            },
        },
        {
            'results': range(100, 110),
            'pagination': {
                'count': 10,
                'last_indexes': {},
            },
        },
    ]
    arg = 'candidates'
    api_key = 'API_KEY'

    # When
    it = filing_iterator.FilingIterator(arg, api_key=api_key)

    # Then
    assert it._endpoint == 'https://api.open.fec.gov/v1/candidates'
    assert it._per_page == 100
    assert it._len == 110
    assert len(it) == 110
    ct = 0
    for i in it:
        assert i == ct
        ct += 1
    assert ct == 110


@mock.patch('requests.get')
def test_filing_iterator_paged(mock_get):
    # Given
    mock_get.return_value.json.side_effect = [
        {
            'results': range(100),
            'pagination': {
                'count': 110,
                'page': 1,
            },
        },
        {
            'results': range(100, 110),
            'pagination': {
                'count': 110,
                'page': 2,
            },
        },
        {
            'results': [],
            'pagination': {
                'count': 110,
                'page': 3,
            },
        },
    ]
    arg = 'candidates'
    api_key = 'API_KEY'

    # When
    it = filing_iterator.FilingIterator(arg, api_key=api_key, paged=True)

    # Then
    assert it._endpoint == 'https://api.open.fec.gov/v1/candidates'
    assert it._per_page == 100
    assert it._len == 110
    assert len(it) == 110
    ct = 0
    for i in it:
        assert i == ct
        ct += 1
    assert ct == 110


@mock.patch('requests.get')
@mock.patch('time.sleep')
def test_filing_iterator_rate_limit(mock_sleep, mock_get):
    # Given
    mock_get.return_value.ok = False
    mock_get.return_value.status_code = 429
    arg = 'candidates'
    api_key = 'API_KEY'

    # When
    with pytest.raises(errors.FecApiError):
        filing_iterator.FilingIterator(arg, api_key=api_key)

    # Then
    for i in range(10):
        assert mock_sleep.called_with(2 ** i)
    assert mock_sleep.call_count == 10


@mock.patch('requests.get')
@mock.patch('time.sleep')
def test_filing_iterator_error(mock_sleep, mock_get):
    # Given
    mock_get.return_value.ok = False
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {'message': 'API error'}
    arg = 'candidates'
    api_key = 'API_KEY'

    # When
    with pytest.raises(errors.FecApiError):
        filing_iterator.FilingIterator(arg, api_key=api_key)

    # Then
    assert mock_sleep.call_count == 0


@mock.patch('requests.get')
@mock.patch('time.sleep')
def test_filing_iterator_misc_error(mock_sleep, mock_get):
    # Given
    mock_get.return_value.ok = False
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {}
    arg = 'candidates'
    api_key = 'API_KEY'

    # When
    with pytest.raises(errors.FecApiError):
        filing_iterator.FilingIterator(arg, api_key=api_key)

    # Then
    assert mock_sleep.call_count == 0
