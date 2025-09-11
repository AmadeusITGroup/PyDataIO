import logging
import os
import shutil

import yaml


def cleanCheckpoint(configPath: str):
    """
    Clean the checkpoint directory
    Args:
        configPath: path to the yaml configuration file

    """
    with open(configPath) as file:
        config = yaml.safe_load(file)

    checkpointPath = config["Output"]["options"].get("checkpointLocation", "")
    if os.path.exists(checkpointPath):
        shutil.rmtree(checkpointPath)
        logging.info("Checkpoint directory %s cleaned", checkpointPath)
    else:
        logging.info("Checkpoint directory %s does not exist", checkpointPath)
