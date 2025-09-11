from abc import ABC, abstractmethod

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


class SinkProcessor(ABC):
    """
    Abstract class to transform data in a forEachBatch context
    """

    @abstractmethod
    def process(self, data: DataFrame):
        pass


class Input(ABC):
    """
    Abstract class to represent an input
    """

    @abstractmethod
    def load(self, spark: SparkSession) -> DataFrame:
        pass


class Output(ABC):
    """
    Abstract class to represent an output
    """

    @abstractmethod
    def build(self, outputConfig: dict):
        pass

    @abstractmethod
    def save(self, data: DataFrame):
        pass
