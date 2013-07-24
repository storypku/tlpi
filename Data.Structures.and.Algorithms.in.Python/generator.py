def factors(n):
    k = 1
    while k * k < n:
        if n % k == 0:
            yield k
            yield n//k
        k += 1
    if k * k == n:
        yield k
def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b
