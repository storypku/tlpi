import time
def log_calls(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        print("Calling {0} with {1} and {2}".format(
            func.__name__, args, kwargs))
        return_value = func(*args, **kwargs)
        print("Executed {0} in {1}ms".format(
            func.__name__, time.time() - now))
        return return_value
    return wrapper

@log_calls
def test1(*args, **kw):
    print("\ttest1 called")

test1(1, 2, 3, a=3, b=2, c=1)

