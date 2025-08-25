import logging

from azure.identity import ClientSecretCredential

from .config_handler import loadConfiguration
from .schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Pipeline class to run the data processing pipeline
    """

    schemaRegistry: SchemaRegistry

    def __init__(self):
        self.schemaRegistry = SchemaRegistry()

    def run(self, confPath: str, credential: ClientSecretCredential = None, additionalArgs: dict = None):
        """
        Run the data processing pipeline
        Args:
            confPath: path to the configuration file
        """
        logger.info("Loading configuration from %s", confPath)
        config = loadConfiguration(confPath, self.schemaRegistry, credential)
        config.transformer.run(config.JobConfig, additionalArgs)
