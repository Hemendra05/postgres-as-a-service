"""
INIT file for the package
"""

import logging
import sys

from .models import DeploymentParams

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)


logger.addHandler(stream_handler)


logger.info("API is starting up")
