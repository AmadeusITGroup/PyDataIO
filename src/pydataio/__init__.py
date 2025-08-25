import logging
from logging.config import fileConfig
import os

# Path to the logging configuration file
config_path = os.path.join(os.path.dirname(__file__), "config", "logging.ini")

logging.info("Config path: %s", config_path)

# Load the logging configuration
fileConfig(config_path)
