import logging
import os

from pyspark.context import SparkContext

from pydataio.pipeline import Pipeline
from tests import root_tests

from . import test_utils
from .dummies import dummyEventSchema

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))


def test_transformer_batch():
    confPath = os.path.join(root_tests, "resources/conf/testConfig.yaml")
    sc = SparkContext.getOrCreate()
    sc.setLogLevel("INFO")
    pipeline = Pipeline()
    pipeline.schemaRegistry.registerSchema("dummyEvent", dummyEventSchema)
    pipeline.run(confPath)

    assert True


def test_transformer_streaming():
    confPath = os.path.join(root_tests, "resources/conf/streamingTestConfig.yaml")
    sc = SparkContext.getOrCreate()
    sc.setLogLevel("INFO")
    pipeline = Pipeline()
    pipeline.schemaRegistry.registerSchema("dummyEvent", dummyEventSchema)
    pipeline.run(confPath)

    test_utils.cleanCheckpoint(confPath)

    assert True


def test_transformer_no_io():
    confPath = os.path.join(root_tests, "resources/conf/testConfigNoIO.yaml")
    sc = SparkContext.getOrCreate()
    sc.setLogLevel("INFO")
    pipeline = Pipeline()
    pipeline.run(confPath)

    assert True


def test_transformer_no_io_add_params():
    confPath = os.path.join(root_tests, "resources/conf/testConfigNoIO.yaml")
    sc = SparkContext.getOrCreate()
    sc.setLogLevel("INFO")
    pipeline = Pipeline()
    pipeline.run(confPath, additionalArgs={"dummyParam": "dummyValue"})

    assert True
