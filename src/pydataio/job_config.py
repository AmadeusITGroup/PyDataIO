from typing import Optional

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from pydataio.io.pipes.spark.batch.inputs import Input
from pydataio.io.pipes.spark.batch.outputs import Output


class JobConfig:
    """
    Class to represent a job configuration
    """

    name: str
    parameters: dict
    reader: Optional[dict[str, Input]]
    writer: Optional[Output]

    def __init__(
        self,
        name: str,
        reader: dict[str, Input],
        writer: Output,
        parameters: dict = None,
    ):
        if parameters is None:
            parameters = {}

        self.name = name
        self.parameters = parameters
        self.reader = reader
        self.writer = writer

    def load(self, inputName: str, spark: SparkSession) -> DataFrame:
        """
        Load a dataframe from an input

        Args:
            inputName: name of the input
            spark: the spark session

        Returns: the dataframe

        """
        if self.reader is None:
            raise ValueError("No reader defined in the configuration")

        return self.reader[inputName].load(spark)
