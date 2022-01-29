import json
import logging

logger = logging.getLogger('NULL')
logger.addHandler(logging.NullHandler())


def handler(event: dict, context):
    logging.info(event)
