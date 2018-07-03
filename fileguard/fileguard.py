from functools import wraps
from types import FunctionType
from collections import defaultdict


class _guard(object):

    def __init__(self, path):
        self._path = path
        self._original = {self._path: []}

    def __call__(self, func):
        if isinstance(func, type):
            return self.decorate_class(func)
        else:
            return self.decorate_callable(func)

    def __enter__(self):
        """Store original file contents"""
        self._store_original_content()
        return self

    def __exit__(self, *exc_info):
        """Restore original file contents"""
        self._restore_original_content()

    def _store_original_content(self):
        path = self._path
        orignal_file_contents = []
        with open(path, 'r') as file:
            for line in file:
                orignal_file_contents.append(line)

        self._original[path].append(orignal_file_contents)

    def _restore_original_content(self):
        path = self._path
        orignal_file_contents = self._original[path].pop()

        with open(path, 'w') as file:
            for line in orignal_file_contents:
                file.write(line)

    def decorate_callable(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.__enter__()
            try:
                return func(*args, **kwargs)
            finally:
                self.__exit__()
        return wrapper

    def decorate_class(self, klass):
        """File Guard every user-defined function in the specified class

        Arguments:
            * klass (class): The class to be file-guarded
        """
        # NOTE: if decorating the __new__ method, keep in mind the following:
        #   * https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
        #   * https://github.com/python/cpython/blob/5a4bbcd479ce86f68bbe12bc8c16e3447f32e13a/Objects/typeobject.c#L3538

        for attr in dir(klass):

            attr_value = getattr(klass, attr)
            if not isinstance(attr_value, FunctionType):
                            continue

            wrapped = self.decorate_callable(attr_value)
            setattr(klass, attr, wrapped)
        return klass

def guard(path):
    """Preserve the contents of a file.

    Can be used as a function decorator, a context manager or a class decorator.
    If used as a class decorator, all user-defined functions will be decorated,
    i.e. all user functions will be file-guarded.

    Args:
        path (path-like): The path of the file to be guarded. It must be
        path-like, such as a string. In general, any object accepted by
        `pathlib.Path` can be used.
    """
    return _guard(path)
