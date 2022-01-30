import json
import logging

# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)

# Retrieve the logger instance
logger = logging.getLogger()


def handler(event, context):
    logger.info(json.dumps(event))
