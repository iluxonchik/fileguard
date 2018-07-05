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


class TestFileGuardContextManager(unittest.TestCase):

    TEST_TEXT_FILE_PATH = './tests/resources/test_text_file.txt'
    TEST_FILE_CONTENTS = ['would\n', 'you do it\n', 'if my name was\n', 'dre\n']

    def setUp(self):
        with open(TestFileGuardContextManager.TEST_TEXT_FILE_PATH, 'w') as file:
            file.writelines(TestFileGuardContextManager.TEST_FILE_CONTENTS)

    def tearDown(self):
        try:
            os.remove(TestFileGuardContextManager.TEST_TEXT_FILE_PATH)
        except FileNotFoundError:
            pass

    def _assert_file_content_equals(self, lines):
        with open(TestFileGuardContextManager.TEST_TEXT_FILE_PATH, 'r') as file:
            file_contents = file.readlines()

        self.assertEqual(len(lines), len(file_contents))

        for i in range(len(lines)):
            self.assertEqual(lines[i], file_contents[i], f'File differs in line {i}')

    def test_guard_change_text_file(self):

        with guard(TestFileGuardContextManager.TEST_TEXT_FILE_PATH):
            lines_to_write = ['of course\n', 'I would\n']
            self._assert_file_content_equals(TestFileGuardContextManager.TEST_FILE_CONTENTS)

            with open(TestFileGuardContextManager.TEST_TEXT_FILE_PATH, 'w') as file:
                file.writelines(lines_to_write)

            self._assert_file_content_equals(lines_to_write)

        self._assert_file_content_equals(TestFileGuardContextManager.TEST_FILE_CONTENTS)


class TestFileGuardClassDecorator(unittest.TestCase):

    TEST_TEXT_FILE_PATH = './tests/resources/test_text_file.txt'
    TEST_FILE_CONTENTS = ['would\n', 'you do it\n', 'if my name was\n', 'dre\n']

    @guard('./tests/resources/test_text_file.txt')
    class TheCodeumentary(object):

        TEXT_1 = ['The\n', 'Documentary\n']
        TEXT_2 = ['The\n', 'Doctor\'s\n', 'Advocate']
        TEXT_3 = ['appended\n', 'content\n']

        def __init__(_self, value_1, value_2, test_case):
            _self._value_1 = value_1
            _self._value_2 = value_2
            _self._test_case = test_case  # allow asserts in methods

        @property
        def value_1(self):
            return self._value_1

        def change_the_file(_self):
            lines_to_write = TestFileGuardClassDecorator.TheCodeumentary.TEXT_1

            with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
                file.writelines(lines_to_write)

            _self._test_case._assert_file_content_equals(TestFileGuardClassDecorator.TheCodeumentary.TEXT_1)

        def change_the_file_again(_self):
            lines_to_write = TestFileGuardClassDecorator.TheCodeumentary.TEXT_2

            with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
                file.writelines(lines_to_write)

            _self._test_case._assert_file_content_equals(TestFileGuardClassDecorator.TheCodeumentary.TEXT_2)

        def do_not_change_the_file(_self, value):
            _self._value_3 = 'L.A.X.'
            _self._value_3 = _self._value_3 + value

        def append_text(_self):
            lines_to_write = TestFileGuardClassDecorator.TheCodeumentary.TEXT_3

            with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'a') as file:
                file.writelines(lines_to_write)

            expected_content = TestFileGuardClassDecorator.TEST_FILE_CONTENTS + lines_to_write + lines_to_write

            _self._test_case._assert_file_content_equals(expected_content)

        def nested_write_call(_self):
            lines_to_write = TestFileGuardClassDecorator.TheCodeumentary.TEXT_3

            with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'a') as file:
                file.writelines(lines_to_write)

            expected_content = TestFileGuardClassDecorator.TEST_FILE_CONTENTS + lines_to_write

            _self._test_case._assert_file_content_equals(expected_content)
            _self.append_text()
            _self._test_case._assert_file_content_equals(expected_content)


    def setUp(self):
        with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'w') as file:
            file.writelines(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

    def tearDown(self):
        try:
            os.remove(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH)
        except FileNotFoundError:
            pass

    def _assert_file_content_equals(self, lines):
        with open(TestFileGuardClassDecorator.TEST_TEXT_FILE_PATH, 'r') as file:
            file_contents = file.readlines()

        self.assertEqual(len(lines), len(file_contents))

        for i in range(len(lines)):
            self.assertEqual(lines[i], file_contents[i], f'File differs in line {i}')

    def test_decorated_class_restores_file_contents(self):
        the_codeumentary = TestFileGuardClassDecorator.TheCodeumentary('value_1', 'value_2', self)
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

        the_codeumentary.change_the_file()
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

        the_codeumentary.change_the_file_again()
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

        the_codeumentary.do_not_change_the_file('hello')
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

        the_codeumentary.value_1
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

        the_codeumentary._value_2 = 'value_3'
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)

    def test_fileguarded_callables_calling_fileguarded_callables(self):
        """
        Make sure that the when a decorated callable calls a decorated callable
        within a class everything works as expectected. Internally, a stack is
        used.
        """
        the_codeumentary = TestFileGuardClassDecorator.TheCodeumentary('value_1', 'value_2', self)
        the_codeumentary.nested_write_call()
        self._assert_file_content_equals(TestFileGuardClassDecorator.TEST_FILE_CONTENTS)
