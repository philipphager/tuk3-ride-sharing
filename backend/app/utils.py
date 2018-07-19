from functools import wraps
from time import time


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result, db_time = f(*args, **kwds)
        elapsed = time() - start
        return {
            'time': elapsed,
            'db_time': db_time,
            'data': result
        }

    return wrapper
