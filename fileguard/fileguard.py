from functools import wraps

def guard(path):
    """Preserve the contents of a file.

    Args:
        path (path-like): The path of the file to be guarded. It must be
        path-like, such as a string. In general, any object accepted by
        `pathlib.Path` can be used.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            orignal_file_contents = []
            with open(path, 'r') as file:
                for line in file:
                    orignal_file_contents.append(line)

            try:
                function(*args, **kwargs)
            except Exception:
                pass

            with open(path, 'w') as file:
                for line in orignal_file_contents:
                    file.write(line)

        return wrapper
    return decorator
