from functools import wraps
from time import time


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        return {
            'time': elapsed,
            'data': result}
    return wrapper
