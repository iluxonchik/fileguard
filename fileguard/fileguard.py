from functools import wraps

class _guard(object):

    def __init__(self, path):
        self._path = path

    def decorate_callable(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = self._path

            orignal_file_contents = []
            with open(path, 'r') as file:
                for line in file:
                    orignal_file_contents.append(line)

            try:
                func(*args, **kwargs)
            except Exception:
                pass

            with open(path, 'w') as file:
                for line in orignal_file_contents:
                    file.write(line)

        return wrapper

    def decorate_class(self):
        raise NotImplemented('Class wrapper not yet implemented.')

    def __call__(self, func):
        if isinstance(func, type):
            return self.decorate_class(func)
        else:
            return self.decorate_callable(func)

def guard(path):
    return _guard(path)
