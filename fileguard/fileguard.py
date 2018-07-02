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

    def _store_original_content(self, path):
        orignal_file_contents = []
        with open(path, 'r') as file:
            for line in file:
                orignal_file_contents.append(line)
        self._original[path] = orignal_file_contents

    def _restore_original_content(self, path):
        orignal_file_contents = self._original[path]

    def _restore_original_file_contents(self, path, orignal_file_contents):
        with open(path, 'w') as file:
            for line in orignal_file_contents:
                file.write(line)

    def decorate_callable(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = self._path

            self._store_original_content(path)

            try:
                func(*args, **kwargs)
            except Exception:
                pass

            self._restore_original_content(path)

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
