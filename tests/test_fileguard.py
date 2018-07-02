import unittest
import os
from unittest.mock import Mock
from fileguard.fileguard import guard

class TestRestoreFileContentsDecorator(unittest.TestCase):

    TEST_TEXT_FILE_PATH = './tests/resources/test_text_file.txt'
    TEST_FILE_CONTENTS = ['would\n', 'you do it\n', 'if my name was\n', 'dre\n']

    def setUp(self):
        with open(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
            file.writelines(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)

    def tearDown(self):
        try:
            os.remove(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH)
        except FileNotFoundError:
            pass

    def _assert_file_content_equals(self, lines):
        with open(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH) as file:
            file_contents = file.readlines()
            self.assertCountEqual(file_contents, lines)

    def test_guard(self):

        @guard(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH)
        def function_that_changes_the_file():
            lines_to_write = ['of course\n', 'I would\n']
            self._assert_file_content_equals(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)

            with open(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH, 'r') as file:
                file.writelines(lines_to_write)

            self._assert_file_content_equals(lines_to_write)

        function_that_changes_the_file()
        self._assert_file_content_equals(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)


    def test_guard_if_function_throws_exception(self):

            @guard(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH)
            def function_that_changes_the_file():
                lines_to_write = ['of course\n', 'I would\n']
                self._assert_file_content_equals(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)

                with open(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH, 'r') as file:
                    file.writelines(lines_to_write)

                self._assert_file_content_equals(lines_to_write)
                raise Exception('Something happened #Windows10')

            function_that_changes_the_file()
            self._assert_file_content_equals(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)


    def test_guard_if_function_not_changes_file(self):

                @guard(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH)
                def function_that_changes_the_file():
                    pass

                function_that_changes_the_file()
                self._assert_file_content_equals(TestRestoreFileContentsDecorator.TEST_FILE_CONTENTS)

    def test_that_decorator_calls_funcion(self):
        value_1 = 'uno'
        value_2 = 'dos'

        mocked_func = Mock()

        guard(TestRestoreFileContentsDecorator.TEST_TEXT_FILE_PATH)(mocked_func)(value_1, value_2)

        mocked_func.assert_called_once_with(value_1, value_2)
