from functools import wraps


class _guard(object):

    def __init__(self, path):
        self._path = path
        self._original = {}

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
        self._original[path] = orignal_file_contents

    def _restore_original_content(self):
        path = self._path
        orignal_file_contents = self._original[path]

        with open(path, 'w') as file:
            for line in orignal_file_contents:
                file.write(line)


    def decorate_callable(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.__enter__()
            try:
                func(*args, **kwargs)
            finally:
                self.__exit__()
        return wrapper

    def decorate_class(self):
        raise NotImplemented('Class wrapper not yet implemented.')

def guard(path):
    """Preserve the contents of a file.

    Args:
        path (path-like): The path of the file to be guarded. It must be
        path-like, such as a string. In general, any object accepted by
        `pathlib.Path` can be used.
    """
    return _guard(path)
