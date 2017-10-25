from collections import defaultdict
import math

def word_probabilities(counts, total_spams,total_non_spams, k = 0.5):
    #Something is fishy here
    spam = 0
    nonSpam = 0
    v = []
    for words in counts:
        w = counts[words]
        spam = w[0] if w.get(0) else 0
        nonSpam = w[1] if w.get(1) else 0
        v.append((words, (spam + k) / (total_spams + 2 * k),
            (nonSpam + k) / (total_non_spams + 2 * k)))
    return v
    #return [(w, (spam + k) / (total_spams + 2 * k),
    #        (non_spam + k) / (total_non_spams + 2 * k))
    #        for w, (spam, non_spam) in counts.items()]

def spam_probability(word_probs, message):
    logProbSpam = logProbNotSpam = 0
    #print(message)
    for word, probSpam, probNotSpam in word_probs:
        if word in message:
            logProbSpam += math.log(probSpam)
            logProbNotSpam += math.log(probNotSpam)
        else:
            logProbSpam += math.log(1 - probSpam)
            logProbNotSpam += math.log(1 - probNotSpam)
    logProbSpam /= 250
    logProbNotSpam /= 250
    probSpam = math.exp(logProbSpam)
    probNotSpam = math.exp(logProbNotSpam)
    #print("Spam:", logProbSpam, probSpam, "Non-Spam:", logProbNotSpam, probNotSpam)
    return probSpam / (probSpam + probNotSpam)

class NaiveBayesClassifier:

    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []

    def train(self, training_set):
        word_counts = defaultdict(dict)
        num_non_spams = num_spams = 0
        length = 0
        for dicts, is_spam in training_set:
            #num_spams += len([element for element in dicts if is_spam])
            for words in dicts:
                length += dicts[words]
                if(is_spam):
                    num_spams += dicts[words]
        #num_spams = len([is_spam for wordDict, is_spam in training_set if is_spam])
        #num_non_spams = length - num_spams

        for dics, is_spam in training_set:
            for words in dicts:
                if(not is_spam):
                    num_non_spams += dicts[words]



        #print(num_spams, ' ', num_non_spams,  ' ', length)
        for dicts, is_spam in training_set:
            for words in dicts:
                if word_counts.get(words, {}).get(0 if is_spam else 1):
                    word_counts[words][0 if is_spam else 1] += dicts[words]
                else:
                    word_counts[words][0 if is_spam else 1] = dicts[words]
        #word_counts = words for words, is_spam in training_set
        self.word_probs = word_probabilities(word_counts, num_spams,
                                             num_non_spams, self.k)

    #We do need a way of finding the probabilities

    def classify(self, message):
        return spam_probability(self.word_probs, message)