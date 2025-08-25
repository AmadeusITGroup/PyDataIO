import logging
from abc import ABC, abstractmethod

from pyspark.sql import SparkSession

from .job_config import JobConfig

logger = logging.getLogger(__name__)


class Transformer(ABC):
    """
    Abstract class for a data transformer
    """

    @abstractmethod
    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        pass

    def run(self, jobConfig: JobConfig, additionalArgs: dict = None):
        """
        Run the transformer
        Args:
            jobConfig: the job configuration
        """
        logger.info("Running transformer %s", jobConfig.name)
        logger.info("Getting spark session")
        sparkSession = SparkSession.builder.appName(jobConfig.name).getOrCreate()
        try:
            logger.info("Running transformer")
            self.featurize(jobConfig, sparkSession, additionalArgs)
        except Exception as e:
            logger.error("Error running transformer %s", e)
            raise e

        logger.info("End of the pipeline")
