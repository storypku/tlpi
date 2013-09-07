import sys

class ClosureInstance:
    def __init__(self, locals_=None):
        if locals_ is None:
            locals_ = sys._getframe(1).f_locals
            print(locals_)
        # Update instance dictionary with callables
        self.__dict__.update((key,value) for key, value in locals_.items()
                             if callable(value) )

    # Redirect special methods
    def __len__(self):
        return self.__dict__['__len__']()

# Example use
def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()

if __name__ == '__main__':
    s = Stack()
    print(s)
    s.push(10)
    s.push(20)
    s.push('Hello')
    print(len(s))
    print(s.pop())
    print(s.pop())
    print(s.pop())
