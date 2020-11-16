# logging
import os
from os import environ

IT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IT_RESOURCES_DIR_NAME = environ.get("RESOURCES_DIR_NAME", default='/resources')
IT_RESOURCES_DIR = environ.get("RESOURCES_DIR", default=IT_BASE_DIR + IT_RESOURCES_DIR_NAME)

OUTPUT_FILE_PREFIX = environ.get("OUTPUT_FILE_PREFIX", default='reverse-')
