from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ("Hello", "world"))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print("Goodbye")

if __name__ == "__main__":
    print("# ---- simple test ---- #")
    test()
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async
    print("# ---- multiprocessing test ---- #")
    test()
