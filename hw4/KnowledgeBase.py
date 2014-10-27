import re

import ConflictResolution
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

def inferPrecedesAndFollows(sentenceArray):
    """Return knowledge of which words precede which"""
    newSentence = []
    for preceding, proceeding in zip(sentenceArray, sentenceArray[1:]):
        newSentence.append(preceding + ' precedes ' + proceeding)
        newSentence.append(proceeding + ' follows ' + preceding)

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

def ORConsequent(name, ruleString, partsOfSpeech, antecedents, consequents):
    """Same thing as ORAntecedent, only creates a generic consequent"""
    OR_edRules = []
    
    for partOfSpeech in partsOfSpeech:
        newConsequent = ruleString.replace('*', partOfSpeech)
        ruleName = name + partOfSpeech + '-Tag'
        OR_edRules.append(Rule(ruleName, antecedents, consequents + [newConsequent]))

    return OR_edRules
"""
Possible (ascending) Order of Complexity:
1.
7.
2.
8.
5. 6.
4.
3.
"""

def applyRelationship1(rules):
    beginRule = Rule("BeginSentence-Tag", ["BEGIN_SENTENCE precedes ?word"], ["?word = Noun", "?word = Pronoun"])
    rules.append(beginRule)

def applyRelationship5and6(rules):
    nounTypesBeforeVerbRules = ORConsequent("NountypeBeforeVerb", "?word1 = *", ("Noun", "Pronoun"), ["?word1 precedes ?word2", "?word2 = Verb"], [])
    for rule in nounTypesBeforeVerbRules:
        rules.append(rule)

def applyRelationship7(rules):
    verbsAfterNounTypesRules = ORAntecedent("VerbAfterNountype", "?word1 = *", ("Noun", "Pronoun"), ["?word1 precedes ?word2"], ["?word2 = Verb"])    
    for rule in verbsAfterNounTypesRules:
        rules.append(rule)

def applyRelationship2(rules):
    adverbAfterVerbRule = Rule("AdverbAfterVerb-Tag", ["?word1 precedes ?word2", "?word1 = Verb"], ["?word2 = Adverb"])
    rules.append(adverbAfterVerbRule)

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
    
    # all the _ preceeds _ relationships
    whatPrecedesAndFollowsFacts = inferPrecedesAndFollows(sentence)
    
    """
    DO THIS IN ResolveConflicts
    # classify known prepositions
    knownPrepositionFacts = [word + ' = Preposition' for word in sentence if word in ALL_PREPOSITIONS]
    # classify -ly adjectives
    ly_AdjectiveFacts = [word + ' = Adjective' for word in sentence if re.search(r'ly$', word)]


    memory = whatPrecedesAndFollowsFacts + knownPrepositionFacts + ly_AdjectiveFacts
    """
    memory = whatPrecedesAndFollowsFacts

    applyRelationship1(Rules)
    applyRelationship2(Rules)
    applyRelationship7(Rules)
    applyRelationship5and6(Rules)

    
    #print memory

    system = RuleBasedSystem(Rules, memory)
    system.generateInferences()
    print ConflictResolution.groupTags(system.workingMemory)
    return system.workingMemory
    
if __name__ == '__main__':
    print('Enter a sentence for the system to tag:')
    inputSentence = raw_input()
    print sanitizedSentence(inputSentence)


