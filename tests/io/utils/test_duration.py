from pydataio.io.utils.duration import parseDuration


def test_parseDuration_hours():
    assert parseDuration("1 hour") == 3600


def test_parseDuration_minutes():
    assert parseDuration("1 minute") == 60


def test_parseDuration_seconds():
    assert parseDuration("1 second") == 1
