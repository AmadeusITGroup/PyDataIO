from abc import ABC, abstractmethod

from pyspark.sql.streaming import DataStreamWriter

from pydataio.io.utils.class_helper import getClass


class StreamingTrigger(ABC):
    """
    Abstract class for a streaming trigger
    """

    @abstractmethod
    def configureTrigger(self, writer: DataStreamWriter):
        pass


class ProcessingTimeTrigger(StreamingTrigger):
    """
    Class to represent a processing time trigger
    """

    interval: str

    def __init__(self, interval: str):
        self.interval = interval

    def configureTrigger(self, writer: DataStreamWriter):
        return writer.trigger(processingTime=self.interval)


class OneTimeTrigger(StreamingTrigger):
    """
    Class to represent a one time trigger
    """

    def configureTrigger(self, writer: DataStreamWriter):
        return writer.trigger(once=True)


class AvailableNowTrigger(StreamingTrigger):
    """
    Class to represent an available now trigger
    """

    def configureTrigger(self, writer: DataStreamWriter):
        return writer.trigger(availableNow=True)


def createtrigger(outputConfig: dict):
    """
    Create the streaming trigger

    Args:
        TriggerClass: the trigger class
        outputConfig: the output configuration

    Returns: the streaming trigger

    """
    triggerType = outputConfig["trigger"]
    TriggerClass = getClass(f"utils.{triggerType}", "triggers")

    if triggerType == "ProcessingTimeTrigger" or triggerType == "ContinuousTrigger":
        return TriggerClass(outputConfig["duration"])
    else:
        return TriggerClass()
