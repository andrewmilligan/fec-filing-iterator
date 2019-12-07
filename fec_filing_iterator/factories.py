'''
.. module:: factories
   :synopsis: Iterator factories that wrap some FEC API endpoints

.. moduleauthor:: Andrew Milligan <andrew.i.milligan@gmail.com>

'''

from .filing_iterator import FilingIterator


def _invalid_type_msg(name, arg, opts):
    '''
    Helper for formatting error messages when an invalid argument is passed to
    an iterator factory.
    '''
    return "invalid {} type '{}' - must be one of {}".format(
        name,
        arg,
        ', '.join([f"'{opt}'" for opt in opts])
    )


def schedules(schedule_type, **kwargs):
    '''
    Iterator factory that creates an iterator to loop through all schedules
    returned from the various FEC schedules endpoints, including
    `/schedules/schedule_a/
    <https://api.open.fec.gov/developers#/receipts/get_schedules_schedule_a_>`_
    and `/schedules/schedule_b/
    <https://api.open.fec.gov/developers#/disbursements/get_schedules_schedule_b_>`_.
    The API has endpoints for schedule types A through F, and this factory
    supports all of them.

    For example, you could get all of the disbursements made by the committee
    Bernie 2020 with:

    >>> bernie_disbursements = []
    >>> for filing in schedules('b', **kwargs):
    ...     bernie_disbursements.append(filing)
    '''
    pagination = {
        'a': False,
        'b': False,
        'c': True,
        'd': True,
        'e': False,
        'f': True,
    }
    sked = schedule_type.lower()
    if sked not in pagination:
        raise ValueError(
            _invalid_type_msg('schedule', sked, pagination)
        )
    return FilingIterator(
        'schedules',
        f'schedule_{sked}',
        paged=pagination[schedule_type],
        **kwargs
    )


def candidates(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through candidates
    returned from the FEC `/canidates/
    <https://api.open.fec.gov/developers#/candidate/get_candidates_>`_
    endpoint. This endpoint allows you to "fetch basic information about
    candidates, and use parameters to filter results to the candidates you're
    looking for".

    Kwargs:
        All keyword arguments are forwarded to the
        :class:`filing_iterator.FilingIterator` object

    For example, you could get each candidate's FEC candidate ID with:

    >>> for cand in candidates(**kwargs):
    ...     print(cand['candidate_id'])
    '''
    return FilingIterator('candidates', paged=True, **kwargs)


def committees(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through committees
    returned from the FEC `/committees/
    <https://api.open.fec.gov/developers#/committee/get_committees_>`_
    endpoint. This endpoint allows you to "fetch basic information about
    committees and filers" and "use parameters to filter for particular
    characteristics".

    Kwargs:
        All keyword arguments are forwarded to the
        :class:`filing_iterator.FilingIterator` object

    For example, you could get each committee's FEC ID with:

    >>> for cmte in committees(**kwargs):
    ...     print(cmte['committee_id'])
    '''
    return FilingIterator('committees', paged=True, **kwargs)


def dates(date_type, **kwargs):
    '''
    Iterator factory that creates an iterator to loop through different kinds
    of dates returned from the FEC API. The API has separate endpoints for
    calendar dates (`/calendar-dates/
    <https://api.open.fec.gov/developers#/dates/get_calendar_dates_>`_),
    election dates (`/election-dates/
    <https://api.open.fec.gov/developers#/dates/get_election_dates_>`_), and
    reporting dates (`/reporting-dates/
    <https://api.open.fec.gov/developers#/dates/get_calendar_dates_>`_), and
    this interator factory supports all three. These endpoints give you access
    to reporting deadlines, election dates, FEC meetings and events, and more.

    Args:
        date_type (str): The type of dates to query ('calendar', 'election', or
        'reporting')

    Kwargs:
        All keyword arguments are forwarded to the
        :class:`filing_iterator.FilingIterator` object

    For example, you could get each election date with:

    >>> for elec in dates('election', **kwargs):
    ...     print(elec['election_date'])
    '''
    valid_types = ['calendar', 'election', 'reporting']
    if date_type not in valid_types:
        raise ValueError(_invalid_type_msg('date', date_type, valid_types))
    return FilingIterator(f"{date_type}-dates", paged=True, **kwargs)


def filings(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through all filings
    returned from the FEC `/filings/
    <https://api.open.fec.gov/developers#/filings/get_filings_>`_ endpoint.
    This endpoint gives you access to "all official records and reports filed
    by or delivered to the FEC".

    For example, you could get each filing's form type with the following
    (though you'll be waiting for a very long time):

    >>> for filing in filings(**kwargs):
    ...     print(filing['form_type'])
    '''
    return FilingIterator('filings', paged=True, **kwargs)
