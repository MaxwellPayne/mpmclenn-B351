import re

from InferenceEngine import *
from Tools import *

ALL_PREPOSITIONS = set()
with open('allprepositions.txt', 'r') as f:
    for preposition in f:
        ALL_PREPOSITIONS.add(preposition.rstrip())

class RuleBasedSystem:
    ###
    # a class defining a production system
    ###
    def __init__(self, rules, workingMemory):
        ###
        # initialization function to do necessary conversions for inference engine
        # and instantiate the production system
        ###
        self.rules = rules
        self.workingMemory = workingMemory

        # necessary for inference engine, NO TOUCHING
        self.workingMemoryList = [parseStringToArray(x) for x in self.workingMemory]

    def generateInferences(self):
        ###
        # calls the inference engine to update the working memory
        ###
        self.workingMemoryList = inferNewFacts(self.rules, self.workingMemoryList)
        self.workingMemory = [parseArrayToString(x) for x in self.workingMemoryList]

class Rule:
    ###
    # a class for holding all of the components of a rule (i.e. name, antecedent, consequents)
    ###
    def __init__(self, name, antecedents, consequents):
        ###
        # initialization function that will convert necessary things for inference
        # engine and instantiate instance of rule
        ###
        self.name = name
        self.antecedents = antecedents
        self.consequents = consequents

        # necessary for inference engine, NO TOUCHING
        self.antecedentList = [parseStringToArray(x) for x in self.antecedents]
        self.consequentList = [parseStringToArray(x) for x in self.consequents]

def inferPrecedes(sentenceArray):
    """Return knowledge of which words precede which"""
    newSentence = []
    for preceding, proceeding in zip(sentenceArray, sentenceArray[1:]):
        newSentence.append(preceding + " precedes " + proceeding)

    return newSentence

def ORAntecedent(name, ruleString, partsOfSpeech, antecedents, consequents):
    """Creates rules for each part of speech in partsOfSpeech by replacing
    the '*' in ruleString with each part and adding the resulting antecedent
    to antecedents"""
    OR_edRules = []

    for partOfSpeech in partsOfSpeech:
        newAntecedent = ruleString.replace('*', partOfSpeech)
        ruleName = name + partOfSpeech + '-Tag'
        OR_edRules.append(Rule(ruleName, antecedents + [newAntecedent], consequents))


    return OR_edRules

def applyRelationship1(rules):
    beginRule = Rule("BeginSentence-Tag", ["BEGIN_SENTENCE precedes ?word"], ["?word = Noun", "?word = Pronoun"])
    rules.append(beginRule)
    
def applyRelationship7(rules):
    verbsAfterNounTypesRules = ORAntecedent("BeforeVerb", "?word1 = *", ("Noun", "Pronoun"), ["?word1 precedes ?word2"], ["?word2 = Verb"])    
    for rule in verbsAfterNounTypesRules:
        rules.append(rule)

def resolveConflicts(memory):
    """Settle disputes when a word is tagged more than once"""
    pass

def sanitizedSentence(inputSentence):
    inputSentence = inputSentence.lower()
    words = parseStringToArray(inputSentence)
    sanitizedWords = []
    
    for word in words:
        word = re.sub(r'[^a-z]', '', word.replace(' ', ''))
        if word: sanitizedWords.append(word)

    return ' '.join(sanitizedWords)
    
    

def tagSentence(sentence):
    ###
    # a function that will take in a sentence and tag it
    ###
    Rules = []
    sentence = parseStringToArray("BEGIN_SENTENCE " + sentence + " END_SENTENCE")
    

    whatPrecedesWhatFacts = inferPrecedes(sentence)
    knownPrepositionFacts = [word + ' = Preposition' for word in sentence if word in ALL_PREPOSITIONS]

    memory = whatPrecedesWhatFacts + knownPrepositionFacts


    applyRelationship1(Rules)
    applyRelationship7(Rules)

    
    #print memory

    system = RuleBasedSystem(Rules, memory)
    system.generateInferences()
    return system.workingMemory
    
if __name__ == '__main__':
    print('Enter a sentence for the system to tag:')
    inputSentence = raw_input()
    print sanitizedSentence(inputSentence)
