from functools import wraps
from collections import defaultdict


class _guard(object):

    """
    Ignored attributes explanation:
        * __class__ - the class to which a class instance belongs. There is no
            need to change that. If changed, it must be assigned a class.
    """
    IGNORED_ATTRS = ['__class__', '__new__']

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
        """File Guard every function call in the specified class"""
        for attr in dir(klass):
            if attr in _guard.IGNORED_ATTRS:
                continue

            attr_value = getattr(klass, attr)

            if not hasattr(attr_value, '__call__'):
                continue

            wrapped = self.decorate_callable(attr_value)
            setattr(klass, attr, wrapped)
        return klass

def guard(path):
    """Preserve the contents of a file.

    Args:
        path (path-like): The path of the file to be guarded. It must be
        path-like, such as a string. In general, any object accepted by
        `pathlib.Path` can be used.
    """
    return _guard(path)
