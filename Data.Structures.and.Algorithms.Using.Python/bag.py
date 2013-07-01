#!/usr/bin/env python3
class _BagIterator:
    def __init__(self, theList):
        self.__items=theList
        self.__curItem = 0
    def __iter__(self):
        return self
    def next(self):
        if self.__curItem < len(self.__items):
            item = self.__items[self.__curItem]
            self.__curItem += 1
            return item
        else:
            raise StopIteration

class Bag:
    def __init__(self):
        self.__items = list()
    def __len__(self):
        return len(self.__items)
    def __contains__(self, item):
        return item in self.__items
    def add(self, item):
        self.__items.append(item)
    def remove(self, item):
        assert item in self.__items, "The item must be in the bag"
        idx = self.__items.index(item)
        return self.__items.pop(idx)
    def __iter__(self):
        return _BagIterator(self.__items)

if __name__ == "__main__":
    mybag = Bag()
    mybag.add(5)
    mybag.add(20)
    mybag.add(10)
    #for item in mybag:
    #    print item
    iterator = mybag.__iter__()
    while True:
        try:
            item = iterator.next()
            print(item)
        except StopIteration:
            break
