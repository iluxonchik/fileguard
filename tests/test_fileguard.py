import unittest
import os
from pathlib import Path
from unittest.mock import Mock
from fileguard.fileguard import guard

class TestFileGuardDecorator(unittest.TestCase):

    TEST_TEXT_FILE_PATH = './tests/resources/test_text_file.txt'
    TEST_FILE_CONTENTS = ['would\n', 'you do it\n', 'if my name was\n', 'dre\n']

    def setUp(self):
        with open(TestFileGuardDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
            file.writelines(TestFileGuardDecorator.TEST_FILE_CONTENTS)

    def tearDown(self):
        try:
            os.remove(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
        except FileNotFoundError:
            pass

    def _assert_file_content_equals(self, lines):
        with open(TestFileGuardDecorator.TEST_TEXT_FILE_PATH, 'r') as file:
            file_contents = file.readlines()

        self.assertEqual(len(lines), len(file_contents))

        for i in range(len(lines)):
            self.assertEqual(lines[i], file_contents[i], f'File differs in line {i}')

    def test_guard_change_text_file(self):
        @guard(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
        def function_that_changes_the_file():
            lines_to_write = ['of course\n', 'I would\n']
            self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)

            with open(TestFileGuardDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
                file.writelines(lines_to_write)

            self._assert_file_content_equals(lines_to_write)

        function_that_changes_the_file()
        self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)


    def test_guard_if_function_throws_exception_text_file(self):
            @guard(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
            def function_that_changes_the_file():
                lines_to_write = ['of course\n', 'I would\n']
                self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)

                with open(TestFileGuardDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
                    file.writelines(lines_to_write)

                self._assert_file_content_equals(lines_to_write)
                raise Exception('Something happened #Windows10')

            with self.assertRaises(Exception):
                function_that_changes_the_file()
            self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)


    def test_guard_if_function_not_changes_text_file(self):

                @guard(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
                def function_that_changes_the_file():
                    pass

                function_that_changes_the_file()
                self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)

    def test_guard_deleted_file_restores_contents_test_file(self):
            @guard(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
            def function_that_deletes_the_file():
                os.remove(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)

                # make sure that the file does not exist after running the function
                is_file = path.is_file()
                self.assertFalse(is_file, 'File does exist.')

            # make sure that the file is existent
            path = Path(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
            is_file = path.is_file()
            self.assertTrue(is_file, 'File does not exist.')

            function_that_deletes_the_file()

            self._assert_file_content_equals(TestFileGuardDecorator.TEST_FILE_CONTENTS)

    def test_that_decorator_calls_funcion(self):
        value_1 = 'uno'
        value_2 = 'dos'

        mocked_func = Mock()

        pre_decorated = guard(TestFileGuardDecorator.TEST_TEXT_FILE_PATH)
        decorated = pre_decorated(mocked_func)
        result = decorated(value_1, value_2)

        mocked_func.assert_called_once_with(value_1, value_2)
