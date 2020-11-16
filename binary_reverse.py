#!$(which python3.7)
import logging as log
import sys

from app.env import LOG_LEVEL
from app.error.errors import UnsupportedBufferSizeException

# init configs
from app.service.file_service import FileService
from app.util.file_utils import MAX_SUPPORTED_BUFFER_SIZE

log.getLogger().setLevel(LOG_LEVEL)


def main(argv):
    try:
        FileService().revers_binary_files(argv, MAX_SUPPORTED_BUFFER_SIZE)
    except (Exception, FileNotFoundError, UnsupportedBufferSizeException) as e:
        log.error(e)


if __name__ == "__main__":
    main(sys.argv[1:])
