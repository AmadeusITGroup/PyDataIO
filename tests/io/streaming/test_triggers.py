import pydataio


def test_createProcessingTimeTrigger():
    conf = {"trigger": "ProcessingTimeTrigger", "duration": "10 seconds"}
    trigger = pydataio.io.utils.triggers.createtrigger(conf)

    assert isinstance(trigger, pydataio.io.utils.triggers.ProcessingTimeTrigger)
    assert trigger.interval == "10 seconds"


def test_createOneTimeTrigger():
    conf = {"trigger": "OneTimeTrigger"}
    trigger = pydataio.io.utils.triggers.createtrigger(conf)

    assert isinstance(trigger, pydataio.io.utils.triggers.OneTimeTrigger)


def test_createAvailableNowTrigger():
    conf = {"trigger": "AvailableNowTrigger"}
    trigger = pydataio.io.utils.triggers.createtrigger(conf)

    assert isinstance(trigger, pydataio.io.utils.triggers.AvailableNowTrigger)


def test_createContinuousTrigger():
    conf = {"trigger": "ContinuousTrigger", "duration": "10 seconds"}

    try:
        pydataio.io.utils.triggers.createtrigger(conf)
        raise AssertionError("Should raise an exception")
    except AttributeError:
        assert True
