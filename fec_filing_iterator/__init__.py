'''A module for iterating though results from the FEC API.

This module provides several useful utilities for iterating through paginated
results from the `FEC API <https://api.open.fec.gov/developers>`_. The meat of
this module is in the :class:`filing_iterator.FilingIterator` class, which
encapsulates the logic of interacting with the FEC API and iterating through
the returned results. In theory the ``FilingIterator`` class can iterate
through the results of any endpoint that the FEC API provides.

Included are several iterator factory functions that allow you to create
instances of the ``FilingIterator`` class to handle common endpoints, such as
those for Schedule A filings. In many cases one of the factory functions will
allow you easy access to the data you need, but if you want access to
a specific endpoint of the API you can always create your own iterator
directly.

.. note::
    All of the factory functions and the ``FilingIterator`` class can be
    imported directly from the top-level of the module, so the following will
    both work:

    >>> from fec_filing_iterator import schedules
    >>> from fec_filing_iterator.factories import candidates

.. moduleauthor:: Andrew Milligan <andrew.i.milligan@gmail.com>

'''

from ._version import __version_info__, __version__  # noqa

from .filing_iterator import FilingIterator # noqa
from .factories import ( # noqa
    candidates,
    committees,
    dates,
    filings,
    schedules,
)
