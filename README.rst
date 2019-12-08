.. image:: https://readthedocs.org/projects/fec-filing-iterator/badge/?version=latest
  :target: https://fec-filing-iterator.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

Overview
========

``fec-filing-iterator`` provides a simple interface for iterating through
results from the `Federal Election Commission's API
<https://api.open.fec.gov/developers>`_ as a single, lazily evaluated stream.
The FEC's API provides access to a wealth of data on where candidates and
committees get their funds, what they spend them on, and more.  This library
simply tries to make the API easier to work with in Python.

Getting Started
---------------

In order to use this library you will first need to get a `data.gov
<https://www.data.gov/>`_ API key, which `you can request here
<https://api.data.gov/signup/>`_. Once you get an API key you will be allowed to
make 1,000 requests to the FEC API per hour.  If you want more throughput you
can request that your key be upgraded to be allowed to make 120 calls per
minute by emailing `APIinfo@fec.gov <mailto:apiinfo@fec.gov>`_ and asking
nicely.

Next, you'll have to install the library::

  pip install fec-filing-iterator

Now you're all set to start exploring campaign finance data! For example::

  import json
  from fec_filing_iterator import schedules

  api_key = '<YOUR_DATA_DOT_GOV_API_KEY>'

  params = {
      'two_year_transaction_period': 2020,
      'committee_id': 'C00696948',
  }

  for filing in schedules('a', api_key=api_key, params=params):
      print(json.dumps(filing, indent=4))

Factories and Iterators
-----------------------

This library only tries to provide an easy way to access and iterate through
the paginated results returned by the FEC API. It does *not* currently attempt
to provide a full and consistent interface for retrieving arbitrary subsets of
information from the API. Lots of powerful searches and queries can be
parameterized through the API, but we leave it up to you to read the `FEC's
documentation <https://api.open.fec.gov/developers>`_ and find the appropriate
parameters yourself.

The main workhorse of the library is the `FilingIterator
<https://fec-filing-iterator.readthedocs.io/en/latest/code.html#module-fec_filing_iterator.filing_iterator>`_
class. Construct it with API credentials, an API endpoint to iterate over, and
whatever parameters you want, and you can treat the full set of records as one
big iterable.

The library also provides several handy factory functions that will construct
the ``FilingIterator`` object and configure it for the appropriate endpoint.
