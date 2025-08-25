from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from pydataio.io.abstract_io import Input
from pyspark.sql.readwriter import DataFrameReader
from pyspark.sql.dataframe import DataFrame


class SparkInput(Input):
    """
    Class to represent a file system input
    """

    format: str
    path: str
    options: dict
    schema: StructType

    def __init__(self, format: str, path: str, options: dict = None, schema: StructType = None):
        if options is None:
            options = {}

        self.format = format
        self.options = options
        self.schema = schema
        self.path = path

    def load(self, spark: SparkSession) -> DataFrame:
        """
        Load a dataframe
        Args:
            spark: the spark session

        Returns: the dataframe

        """
        reader: DataFrameReader = spark.read.format(self.format).options(**self.options)

        if self.schema is not None:
            reader = reader.schema(self.schema)

        return reader.load(self.path)
