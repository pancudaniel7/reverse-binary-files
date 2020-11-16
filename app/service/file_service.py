import logging as log
import os
from os import path

from singleton_decorator import singleton

from app.env import OUTPUT_FILE_PREFIX
from app.util.file_utils import FileUtils


@singleton
class FileService:

    def revers_binary_files(self, file_paths, copy_buffer_size: int):
        for file_path in file_paths:
            self.reverse_binary_file(file_path, copy_buffer_size)

    def reverse_binary_file(self, input_file_path: str, copy_buffer_size: int):
        if not path.isfile(input_file_path):
            log.error("File not found for path: {}".format(input_file_path))
        else:
            output_file_path = self.__create_output_file_path(input_file_path)
            FileUtils.write_reverse_binary(input_file_path, output_file_path, copy_buffer_size)
            log.debug('Finish reversing and write binaries for file: {}'.format(input_file_path))

    def __create_output_file_path(self, file_path: str) -> str:
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        output_file_name = '{}'.format(OUTPUT_FILE_PREFIX) + file_name
        return dir_name + output_file_name
