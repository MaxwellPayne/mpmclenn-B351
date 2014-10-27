
_allPrepositions = set()
with open('allprepositions.txt', 'r') as f:
    for preposition in f:
        _allPrepositions.add(preposition.rstrip())

_allDeterminers = set()
with open('alldeterminers.txt', 'r') as f:
    for determiner in f:
        _allDeterminers.add(determiner.rstrip())

_allPronouns = set()
with open('allpronouns.txt', 'r') as f:
    for preposition in f:
        _allPronouns.add(preposition.rstrip())

def isPreposition(word):
    return word in _allPrepositions

def isDeterminer(word):
    return word in _allDeterminers

def isPronoun(word):
    return word in _allPronouns

if __name__ == '__main__':
    ambiguousPronounPreps = allPrepositions & allPronouns
    for ambig in ambiguousPronounPreps:
        print ambig
    print 'There are %d ambiguous pronoun-prepositions' % len(ambiguousPronounPreps)
