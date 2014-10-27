
def groupTags(workingMemory):
    tags = filter(lambda fact: '=' in fact, workingMemory)
    taggedWords = {}

    for tag in tags:
        # group all possible classifications by word
        word, part = tuple(tag.split(' = '))
        if word in taggedWords:
            taggedWords[word].append(part)
        else:
            taggedWords[word] = [part]

    for word in taggedWords:
        # remove duplicates
        taggedWords[word] = list(set(taggedWords[word]))

    tokenWords = ("BEGIN_SENTENCE", "END_SENTENCE")
    # if system tagged token words, forget them
    for token in tokenWords:
        if token in taggedWords:
            del taggedWords[token]

    return taggedWords

def resolve(taggedSentence):
    """Aggregates all conflict resolution rules
    into a single function"""
    pass

if __name__ == '__main__':
    pass
