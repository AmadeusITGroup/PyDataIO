import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
)

from pydataio.io.abstract_io import SinkProcessor
from pydataio.job_config import JobConfig
from pydataio.transformer import Transformer

logger = logging.getLogger(__name__)


class DummyProcessor(SinkProcessor):
    """
    Dummy processor for test purpose
    """

    def process(self, data: DataFrame):
        logger.info("Processing data with %s rows", data.count())
        return data


class DummyTransformer(Transformer):
    """
    Dummy transformer for test purpose
    """

    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        events = jobConfig.load(inputName="events", spark=spark)

        events.groupBy("id").count()

        jobConfig.writer.save(data=events)


class DummyTransformerNoIO(Transformer):
    """
    Dummy transformer without input output for test purpose
    """

    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        logger.info("Featurizing data without IO from %s", jobConfig.parameters["dummyParam"])


dummyEventSchema = StructType(
    [
        StructField("id", StringType(), False),
        StructField("phase", StringType(), True),
        StructField("value", StringType(), True),
    ]
)
