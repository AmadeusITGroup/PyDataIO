import logging
import uuid
from importlib import import_module

from pyspark.sql import DataFrame
from pyspark.sql.streaming import DataStreamWriter

from pydataio.io.abstract_io import Output
from pydataio.io.abstract_io import SinkProcessor
from pydataio.io.utils.duration import parseDuration
from pydataio.io.utils.triggers import StreamingTrigger
from pydataio.io.utils.triggers import createtrigger

logger = logging.getLogger(__name__)


class SparkOutput(Output):
    """
    Class to represent a file system streaming output
    """

    format: str
    mode: str
    path: str
    partitionColumn: str
    timeout: int
    trigger: StreamingTrigger
    options: dict
    outputName: str
    sinkProcessor: SinkProcessor

    def build(self, outputConfig: dict):
        """
        Build the output
        Args:
            outputConfig: the output configuration

        """

        self.format = outputConfig["format"]
        self.mode = outputConfig["mode"]
        self.path = outputConfig["path"]
        self.timeout = parseDuration(outputConfig["timeout"])
        self.outputName = outputConfig["name"]
        self.trigger = createtrigger(outputConfig)
        self.partitionColumn = outputConfig.get("partitionColumn")
        self.options = outputConfig.get("options", {})
        self.sinkProcessor = self.createSinkTransformer(outputConfig)

        return self

    def createSinkTransformer(self, outputConfig: dict):
        """
        Create the sink transformer
        Args:
            outputConfig: the output configuration

        Returns: the sink transformer

        """
        sinkProcessorParam = outputConfig.get("sinkProcessor")
        if sinkProcessorParam is not None:
            logger.info("Using sink transformer %s", sinkProcessorParam)
            processorModulePath, processorClass = sinkProcessorParam.rsplit(".", 1)

            processorModule = import_module(processorModulePath)
            processor = getattr(processorModule, processorClass)
            return processor()
        else:
            return None

    def save(self, data: DataFrame):
        """
        Save the dataframe
        Args:
            data: the dataframe to save

        """
        logger.info("Saving dataframe to %s, format: %s, mode: %s, trigger: %s, partitionColumn: %s, options: %s", self.path, self.format, self.mode, self.trigger, self.partitionColumn, self.options)
        writer = data.writeStream.format(self.format).options(**self.options).outputMode(self.mode).queryName(self.createQueryName())
        writer = self.trigger.configureTrigger(writer)

        if self.partitionColumn is not None:
            logger.info("Partitioning by %s", self.partitionColumn)
            writer = writer.partitionBy(self.partitionColumn)

        if self.sinkProcessor is not None:
            writer = self.setupSinkProcessor(writer)

        logger.info("Saving to %s", self.path)
        streamingQuery = writer.start(self.path)
        streamingQuery.awaitTermination(timeout=self.timeout)

        streamingQuery.stop()

    def setupSinkProcessor(self, writer: DataStreamWriter):
        """
        Setup the sink processor
        Args:
            writer: the streaming writer

        Returns: the streaming writer with for each batch configured

        """
        logger.info("Setting for each batch processor %s", self.sinkProcessor)

        def writeBatch(dataFrame, batchId):
            resultDataFrame = self.sinkProcessor.process(dataFrame)
            resultDataFrame.write.format(self.format).options(**self.options).mode(self.mode).save(self.path)

        return writer.foreachBatch(writeBatch)

    def createQueryName(self):
        """
        Create a query name
        Returns: the query name

        """
        return f"QN_{self.outputName}_{uuid.uuid4()}"
