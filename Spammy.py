import NaiveBayes
from NaiveBayes import NaiveBayesClassifier
import json

FIND = []#["BarackObama", "HillaryClinton", "RealDonaldTrump"]
TRAIN = ["HillaryClinton", "cbellantoni", "Atrios", "nicopitney", "ggreenwald", 
          "wonkroom", "stevebenen", "AlanColmes", "nathandaschle", "ewerickson",
          "mindyfinn", "dmataconis", "TPCarney", "jbarro", "Heminator", 
          "reihansalam", "RepublicanStudy", "RealDonaldTrump"]
REP = ["ewerickson", "mindyfinn", "dmataconis", "TPCarney", "jbarro", "Heminator",
       "reihansalam", "RepublicanStudy", "RealDonaldTrump"]

with open("accounts.json") as findFile:
    FIND = (json.loads(findFile.read()))

training = []
#classifying = []
spammy = NaiveBayesClassifier()
for user in TRAIN:
    with open(user + ".json") as inFile:
        training.append((json.loads(inFile.read()), False if user in REP else True))
#Find the prob of 'spam'
#print(training)
spammy.train(training)
#print(spammy.word_probs)
for user in FIND:
    classifying = []
    with open(user + "Set.json") as inFile:
        classifying = json.loads(inFile.read())
    spammy.classify(classifying)
    #print(classifying)
    print("Percent of @" + user, "being Democrat: ", "{0:.2f}".format(spammy.classify(classifying)*100), "%")