import os

from cffi.backend_ctypes import xrange
from singleton_decorator import singleton

from app.error.errors import UnsupportedBufferSizeException

MAX_SUPPORTED_BUFFER_SIZE: int = 30
MIN_SUPPORTED_BUFFER_SIZE: int = 7


@singleton
class FileUtils:

    def __check_buffer_size(self, buffer_size):
        if not MIN_SUPPORTED_BUFFER_SIZE <= buffer_size <= MAX_SUPPORTED_BUFFER_SIZE:
            raise UnsupportedBufferSizeException("Buffer size error, buffer size show be between {} and {} values!"
                                                 .format(MIN_SUPPORTED_BUFFER_SIZE, MAX_SUPPORTED_BUFFER_SIZE))

    def write_reverse_binary(self, input_file_path: str, output_file_path: str, buffer_size: int):
        """
        Write reverse binary from input file to output file

        :param input_file_path: the input file path
        :param output_file_path: the output file path
        :param buffer_size: buffer chuck size.
        """
        self.__check_buffer_size(buffer_size)
        buffer_size = 1 << buffer_size

        with open(input_file_path, 'rb') as file, \
                open(output_file_path, 'wb') as file_out:
            file.seek(0, os.SEEK_END)
            for cursor_position in reversed(xrange(0, file.tell(), buffer_size)):
                file.seek(cursor_position, os.SEEK_SET)
                file_out.write(file.read(buffer_size)[::-1])
