import filecmp
import logging
import os
import shutil
import tempfile
import unittest

from app.error.errors import UnsupportedBufferSizeException
from app.service.file_service import FileService
from app.util.file_utils import MAX_SUPPORTED_BUFFER_SIZE
from tests.integration.env import IT_RESOURCES_DIR, OUTPUT_FILE_PREFIX

RANDOM_BASE64_LARGE_FILE_PATH = '{}/50mRandomBase64.dat'.format(IT_RESOURCES_DIR)
RANDOM_BASE64_SMALL_FILE_PATH = '{}/500bRandomBase64.dat'.format(IT_RESOURCES_DIR)


class BinaryReverseTestCase(unittest.TestCase):
    random_500b_file_path = '{}/500bRandomBase64.dat'.format(IT_RESOURCES_DIR)

    def setUp(self):
        self.base64_50m_file = open(RANDOM_BASE64_LARGE_FILE_PATH)
        self.base64_500b_file = open(RANDOM_BASE64_SMALL_FILE_PATH)

    def tearDown(self):
        self.base64_50m_file.close()
        self.base64_500b_file.close()

    def __create_temp_file_path(self, file_path) -> str:
        temp_dir = tempfile.gettempdir()
        input_file_name = os.path.basename(file_path)
        return os.path.join(temp_dir, input_file_name)

    def __create_temp_file_copy(self, input_file_path: str) -> str:
        temp_file_path = self.__create_temp_file_path(input_file_path)
        shutil.copy2(input_file_path, temp_file_path)
        return temp_file_path

    def __create_reverse_temp_file_path(self, input_temp_file_path, reverse_file_prefix: str) -> str:
        input_temp_file_path, input_temp_file_name = os.path.split(input_temp_file_path)
        output_temp_file_name = '/{}{}'.format(reverse_file_prefix, input_temp_file_name)
        return input_temp_file_path + output_temp_file_name

    def __create_single_reverse_and_initial_file(self, input_temp_file_path):
        # trigger reverse binary file creation
        FileService().reverse_binary_file(input_temp_file_path, MAX_SUPPORTED_BUFFER_SIZE)

        # reverse process by creating initial file from the reverse file
        output_temp_file_path = self.__create_reverse_temp_file_path(input_temp_file_path, OUTPUT_FILE_PREFIX)
        FileService().reverse_binary_file(output_temp_file_path, MAX_SUPPORTED_BUFFER_SIZE)

        # return created reverse file path
        return self.__create_reverse_temp_file_path(output_temp_file_path, OUTPUT_FILE_PREFIX)

    def test_binary_reverse_file_process(self):
        """
        Test binary for large and small file
        """
        input_large_temp_file_path = self.__create_temp_file_copy(RANDOM_BASE64_LARGE_FILE_PATH)
        input_small_temp_file_path = self.__create_temp_file_copy(RANDOM_BASE64_SMALL_FILE_PATH)

        new_reversed_large_temp_file_path = self.__create_single_reverse_and_initial_file(input_large_temp_file_path)
        new_reversed_small_temp_file_path = self.__create_single_reverse_and_initial_file(input_small_temp_file_path)

        # check if the file was reverse correctly to know if reverse binary functionality works
        self.assertTrue(filecmp.cmp(input_large_temp_file_path, new_reversed_large_temp_file_path))
        self.assertTrue(filecmp.cmp(input_small_temp_file_path, new_reversed_small_temp_file_path))

    def test_binary_reverse_multiple_files_process(self):
        """
        Test binary for multiple files created at once
        """
        input_large_temp_file_path = self.__create_temp_file_copy(RANDOM_BASE64_LARGE_FILE_PATH)
        input_small_temp_file_path = self.__create_temp_file_copy(RANDOM_BASE64_SMALL_FILE_PATH)

        input_temp_files = (input_large_temp_file_path, input_small_temp_file_path)
        FileService().revers_binary_files(input_temp_files, MAX_SUPPORTED_BUFFER_SIZE)

        new_reversed_large_temp_file_path = self.__create_single_reverse_and_initial_file(input_large_temp_file_path)
        new_reversed_small_temp_file_path = self.__create_single_reverse_and_initial_file(input_small_temp_file_path)

        # check if the file was reverse correctly to know if reverse binary functionality works
        self.assertTrue(filecmp.cmp(input_large_temp_file_path, new_reversed_large_temp_file_path))
        self.assertTrue(filecmp.cmp(input_small_temp_file_path, new_reversed_small_temp_file_path))

    def test_binary_reverse_with_unsupported_buffer_size(self):
        """
        Test reverse binary when it raise UnsupportedBufferSizeException
        """
        wrong_buffer_size = 199
        input_large_temp_file_path = self.__create_temp_file_copy(RANDOM_BASE64_LARGE_FILE_PATH)

        with self.assertRaises(UnsupportedBufferSizeException):
            FileService().reverse_binary_file(input_large_temp_file_path, wrong_buffer_size)

    def test_binary_reverse_when_file_is_not_found(self):
        """
        Test if service when it raise FileNotFoundError
        """
        notfound_input_large_temp_file_path = '/wrong/file'

        with self.assertLogs('root', logging.DEBUG) as context:
            logging.getLogger('root').error('File not found for path: {}'.format(notfound_input_large_temp_file_path))
        self.assertEqual(context.output,
                         ['ERROR:root:File not found for path: {}'.format(notfound_input_large_temp_file_path)])
