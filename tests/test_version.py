from fec_filing_iterator import _version as version


def test_version():
    assert len(version.__version_info__) == 3
