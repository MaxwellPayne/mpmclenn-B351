from math import factorial
from itertools import chain

# 1.
"""
I believe that ALICE has a few rules that govern its behavior, and that it responds to each sentence by analyzing the sentence, finding pre-defined patterns in the sentence, and assigning a pre-written response to the matched pattern. I think words like 'where' 'who' and 'why,' as well as the existence of a '?' trigger pattern matches. Based on my experience, it does not appear that ALICE uses any sort of artificial intelligence like machine learning; it seems as though both its rules and responses are hard-coded.
"""

# 2.
"""
ALICE's responses seem limited and repetitive. It is fairly easy to get it to use the same reply word-for-word at different points in a conversation. It could diversify its vocabulary by picking up phrases from users. When it asks questions of users, it could look at user replies and save those for use in similar cases. If it were asking questions about age, for example, it could discern whether or not the user gave a sincere reply, and if so, record the semantics of the response for use later when a differnt user asks it a similar question.
"""

# 3.
"""
The latter statement is true; modern computers follow instructions programmed by humans and nothing more. But even if computers 'can only do what their programmers tell them,' whether or not they can be intelligent depends entirely upon the definition of intelligence. If intelligence is the ability to learn and respond to new situations, then computers can certainly be intelligent. Computers can use genetic algorithms to improve their abilities in certain areas, and can record past successes and failures in their file systems that influence later behavior. But if intelligence is defined as the ability to create abstract thought, then the answer is less clear. One must investigate the nature of conciousness, and question whether or not humans actually have the ability to create abstract thought. 
"""

# 4.
"""
(42,000 students and faculty) * (2% buying a Starbucks coffee on any given weekday) * (70% of coffees ordered that are lattes) = 588 lattes per weekday
(42,000 students and faculty) * (0.5% buying a Startucks coffee on any given weekend day) * (70% of coffees ordered that are lattes) = 147 lattes per weekend day

(16 weeks) * ( (5 weekdays * 588 lattes) + (2 weekend days * 147 lattes) ) = 51,744 lattes per semester

For an AI system to do this sort of abstract calculation, it would need to figure out a population size, rate of consumption, and time frame. Breaking a semester down into weeks and days would be trivial. Population data is fairly availible as well; the rate of consumption would be the hard variable to estimate. An AI system could best estimate this by learning from other estimation experiments. If it were trained to scrape the web for corporate sales data, for example, then break that sales data down into smaller units such as store location, it could apply these experiences to Starbucks' operations in Bloomington.
"""

# 5.
def function1(unsortedList):
    """A recursive mergesort function"""
    
    def merge(left, right):
        # merges two sorted lists into one
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
        # base case: list is 'sorted' b/c single-element or empty
        return unsortedList
    else:
        # cut list in half, recursively sort both halves, merge
        middle = len(unsortedList) / 2
        l, r = function1(unsortedList[:middle]), function1(unsortedList[middle:])
        return merge(l, r)


# 6.
def function2(listToCount, searchElement):
    """Recursively cuts sorted lists in half, throws them away if
    they can't contain searchElement, recursively counts them if they can"""
    def recur(ls, count):
        # base cases: count empty and one-element lists
        if len(ls) == 0: return count
        elif len(ls) == 1: return int(ls[0] == searchElement)
        newCount = count
        middle = len(ls) / 2
        left, right = ls[middle:], ls[:middle]
        # divide the list in two
        if right[-1] >= searchElement:
            # for right list: if last element gt searchElement,
            # searchElement might exist in it, so search
            newCount += recur(right, count)
        if left[0] <= searchElement:
            # for left list: if first element lt searchElement,
            # searchElement might exist in it, so search
            newCount += recur(left, count)
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
