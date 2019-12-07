import pytest
import mock
from fec_filing_iterator import factories


@mock.patch('fec_filing_iterator.factories.FilingIterator')
def test_schedules(mock_iter):
    '''
    Creates a FilingIterator with the right endpoint and pagination
    '''
    # Given
    skeds = {
        'a': False,
        'b': False,
        'c': True,
        'd': True,
        'e': False,
        'f': True,
    }
    kwargs = {'api_key': 'API_KEY'}

    for sked, paged in skeds.items():
        # When
        factories.schedules(sked, **kwargs)

        # Then
        mock_iter.assert_called_with(
            'schedules',
            f'schedule_{sked}',
            paged=paged,
            **kwargs
        )


def test_schedules_fail():
    '''
    Raises when given a bad schedule
    '''
    # Given
    sked = 'x'

    with pytest.raises(ValueError):
        factories.schedules(sked)


@mock.patch('fec_filing_iterator.factories.FilingIterator')
def test_candidates(mock_iter):
    '''
    Creates a FilingIterator with the right endpoint and pagination
    '''
    # Given
    kwargs = {'api_key': 'API_KEY'}

    # When
    factories.candidates(**kwargs)

    # Then
    mock_iter.assert_called_with('candidates', paged=True, **kwargs)


@mock.patch('fec_filing_iterator.factories.FilingIterator')
def test_committees(mock_iter):
    '''
    Creates a FilingIterator with the right endpoint and pagination
    '''
    # Given
    kwargs = {'api_key': 'API_KEY'}

    # When
    factories.committees(**kwargs)

    # Then
    mock_iter.assert_called_with('committees', paged=True, **kwargs)


@mock.patch('fec_filing_iterator.factories.FilingIterator')
def test_dates(mock_iter):
    '''
    Creates a FilingIterator with the right endpoint and pagination
    '''
    # Given
    dates = ['calendar', 'election', 'reporting']
    kwargs = {'api_key': 'API_KEY'}

    for date in dates:
        # When
        factories.dates(date, **kwargs)

        # Then
        mock_iter.assert_called_with(
            f'{date}-dates',
            paged=True,
            **kwargs
        )


def test_dates_fail():
    '''
    Raises when given a bad date
    '''
    # Given
    date = 'x'

    with pytest.raises(ValueError):
        factories.dates(date)


@mock.patch('fec_filing_iterator.factories.FilingIterator')
def test_filings(mock_iter):
    '''
    Creates a FilingIterator with the right endpoint and pagination
    '''
    # Given
    kwargs = {'api_key': 'API_KEY'}

    # When
    factories.filings(**kwargs)

    # Then
    mock_iter.assert_called_with('filings', paged=True, **kwargs)
