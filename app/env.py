from os import environ

LOG_LEVEL = environ.get("LOG_LEVEL", default='INFO')
OUTPUT_FILE_PREFIX = environ.get("OUTPUT_FILE_PREFIX", default='reverse-')
