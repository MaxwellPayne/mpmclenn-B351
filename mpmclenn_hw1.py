from math import factorial
from itertools import chain

# 5.
def function1(unsortedList):

    
    def merge(left, right):
        merged = []
        l, r = 0, 0
        while (l < len(left) and r < len(right)):
            if left[l] < right[r]:
                merged.append(left[l])
                l += 1
            else:
                merged.append(right[r])
                r += 1
            
        remaining = left[l:] if r > l else right[r:]
        return merged + remaining
        

    if len(unsortedList) <= 1:
        return unsortedList
    else:
        middle = len(unsortedList) / 2
        l, r = function1(unsortedList[:middle]), function1(unsortedList[middle:])
        return merge(l, r)


# 6.
def function2(listToCount, searchElement):
    
    def recur(ls, count):
        if len(ls) == 0: return count
        elif len(ls) == 1: return int(ls[0] == searchElement)
        newCount = count
        middle = len(ls) / 2
        left, right = ls[:middle], ls[middle:]
        if left[-1] >= searchElement:
            newCount += recur(left, count)
        if right[0] <= searchElement:
            newCount += recur(right, count)
        return newCount

    return recur(listToCount, 0)


def nCr(n, r):
    return factorial(n) / (factorial(r) * factorial(n-r))


# 7.
def function3(toDepth):

    def layer(depth):
        return map(lambda r: nCr(depth, r), xrange(depth+1))

    layers = [layer(d) for d in xrange(toDepth+1)]
    layerLength = len(str(layers[-1])) + len(layers[-1]) - 1
    
    for l in layers:
        print ' '.join(map(str, l)).center(layerLength)



def _main():
    print function2([1, 1, 2, 4], 8)
    print function2([1, 2, 2, 3, 5, 5, 6], 5)

    print function1([1, 4, 2, 1])
    print function1([1, 5, 5, 3, 2, 6, 2])

    function3(10)


if __name__ == '__main__':
    _main()
