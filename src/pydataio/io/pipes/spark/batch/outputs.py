import logging

from pyspark.sql import DataFrame

from pydataio.io.abstract_io import Output

logger = logging.getLogger(__name__)


class SparkOutput(Output):
    """
    Class to represent a file system output
    """

    format: str
    mode: str
    path: str
    partitionColumn: str
    options: dict

    def build(self, outputConfig: dict):
        """
        Build the output
        Args:
            outputConfig: the output configuration

        """
        self.format = outputConfig["format"]
        self.mode = outputConfig["mode"]
        self.path = outputConfig["path"]
        self.partitionColumn = outputConfig.get("partitionColumn")
        self.options = outputConfig.get("options", {})

        return self

    def save(self, data: DataFrame):
        """
        Save the dataframe
        Args:
            data: the dataframe to save

        """

        logger.info("Saving dataframe to %s, format: $s, mode: %s, partitionColumn: %s, options: %s", self.path, self.format, self.mode, self.partitionColumn, self.options)
        writer = data.write.format(self.format).options(**self.options).mode(self.mode)

        if self.partitionColumn is not None:
            logger.info("Partitioning by %s", self.partitionColumn)
            writer = writer.partitionBy(self.partitionColumn)

        logger.info("Saving to %s", self.path)
        return writer.save(self.path)
