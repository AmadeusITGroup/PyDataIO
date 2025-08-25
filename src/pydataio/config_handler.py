import logging
from importlib import import_module
from typing import Optional
from urllib.parse import urlparse

import fsspec
import yaml
from azure.identity import ClientSecretCredential

from pydataio.io.pipes.spark.batch.inputs import Input
from pydataio.io.pipes.spark.batch.outputs import Output
from .io.utils.class_helper import getClass
from .job_config import JobConfig
from .pipeline_config import PipelineConfig
from .schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)


def loadConfiguration(configPath: str, schemaRegistry: SchemaRegistry, credential: ClientSecretCredential = None):
    """
    Load a yaml configuration file from a path
    Args:
        configPath: path to the yaml configuration file

    Returns: JobConfig object

    """
    config = parse_config(configPath, credential)

    transformerModulePath, transformerClass = config["Processing"]["type"].rsplit(".", 1)
    transformerModule = import_module(transformerModulePath)
    transformer = getattr(transformerModule, transformerClass)

    reader = buildInput(config.get("Input", None), schemaRegistry)
    writer = buildOutput(config.get("Output", None))

    jobConfig = JobConfig(
        name=transformerClass,
        reader=reader,
        writer=writer,
        parameters=config["Processing"].get("parameters", None),
    )
    return PipelineConfig(transformer=transformer(), JobConfig=jobConfig)


def parse_config(configPath: str, credential: ClientSecretCredential = None):
    """
    Load and parse a YAML configuration file from a given path.

    Args:
        configPath (str): Path to the YAML configuration file.
        credential (ClientSecretCredential, optional): Credential for accessing Azure Blob Storage.

    Returns:
        dict: Parsed configuration as a dictionary.
    """
    logger.info("Loading configuration from %s", configPath)

    parsed_url = urlparse(configPath)
    if parsed_url.scheme == "abfss":
        dfs_core_windows_net = ".dfs.core.windows.net"
        assert dfs_core_windows_net in parsed_url.hostname
        storage_account_name = parsed_url.hostname.split(dfs_core_windows_net)[0]

        fsspec_handle = fsspec.open(
            configPath,
            mode="rt",
            account_name=storage_account_name,
            credential=credential,
        )
    else:
        fsspec_handle = fsspec.open(configPath, mode="rt")

    with fsspec_handle.open() as file:
        config = yaml.safe_load(file)
    logger.info("Configuration parsed: %s", config)
    return config


def buildInput(inputConfig: Optional[list[dict]], schemaRegistry: SchemaRegistry) -> Optional[dict[str, Input]]:
    """
    Build an Input object from a dictionary
    Args:
        inputConfig: dictionary containing the configuration for the FileSystemInput object

    Returns: the FileSystemInput object

    """
    if inputConfig is None:
        logger.warning("No input configuration found!")
        return None

    inputs = {}

    for input in inputConfig:
        ReaderClass = getClass(input["type"], "inputs")
        inputs[input["name"]] = ReaderClass(
            format=input["format"],
            path=input["path"],
            options=input.get("options", None),
            schema=schemaRegistry.get_schema(input.get("schema", "")),
        )

    return inputs


def buildOutput(outputConfig: Optional[dict]) -> Optional[Output]:
    """
    Build an Output object from a dictionary
    Args:
        outputConfig: dictionary containing the configuration for the FileSystemOutput object

    Returns: the FileSystemOutput object

    """
    if outputConfig is None:
        logger.warning("No output configuration found!")
        return None

    WriterClass = getClass(outputConfig["type"], "outputs")

    return WriterClass().build(outputConfig)
