from filing_iterator import FilingIterator


def invalid_type_msg(name, arg, opts):
    '''
    Helper for formatting error messages when an invalid argument is passed to
    an iterator factory
    '''
    return "invalid {} type '{}' - must be one of {}".format(
        name,
        arg,
        ', '.join([f"'{opt}'" for opt in opts])
    )


def candidates(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through candidates
    returned from the FEC `/caniddates/` endpoint.
    '''
    return FilingIterator('candidates', paged=True, **kwargs)


def committees(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through committees
    returned from the FEC `/committees/` endpoint.
    '''
    return FilingIterator('committees', paged=True, **kwargs)


def dates(date_type, **kwargs):
    '''
    Iterator factory that creates an iterator to loop through different kinds
    of dates returned from the FEC API. The API has separate endpoints for
    'calendar' dates (`/calendar-dates/`), 'election' dates
    (`/election-dates/`), and 'reporting' dates (`/reporting-dates`), and this
    interator factory supports all three.
    '''
    valid_types = ['calendar', 'election', 'reporting']
    if not date_type in valid_types:
        raise ValueError(invalid_type_msg('date', date_type, valid_types))
    return FilingIterator(f"{date_type}-dates", paged=True, **kwargs)


def filings(**kwargs):
    '''
    Iterator factory that creates an iterator to loop through all filings
    returned from the FEC `/filings/` endpoint.
    '''
    return FilingIterator('filings', paged=True, **kwargs)


def schedule(schedule_type, **kwargs):
    '''
    Iterator factory that creates an iterator to loop through all schedules
    returned from the FEC `/schedules/` endpoints. The API has endpoints for
    schedule types A through F, and this factory supports all of them.
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
    if not sked in pagination:
        raise ValueError(
            invalid_type_msg('schedule', sked, pagination)
        )
    return FilingIterator(
        'schedules',
        f'schedule_{sked}',
        paged=pagination[schedule_type],
        **kwargs
    )
