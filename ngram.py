import sys, math

class Ngram:

    #n: number of grams (1 = unigram, 2 = bigram, etc.)
    #text: a text corpus to model
    #smoothingBound: smooth all words that appear less than the smoothingBound (with Good Turing smoothing)
    #Returns a dictionary with keys that strings representing lists of words, and values that are counts
    #To-do: Split this into more modular functions.
    def __init__(self, n, text, smoothingBound ):
        self.n = n
        self.total_grams = 0
        self.unique_words = 0
        self.dictionary = {}
        self.smoothing_bound = smoothingBound
        #count_list is an array containing the counts of low frequency ngrams
        #for example, count_list[1] contains the number of unique ngrams that appear exactly 1 time
        self.count_list= [0]*(self.smoothing_bound + 1)
        unique_ngrams = 0
        self.vocab = set()
        previous = list()   # Sentences are NOT independent of one another. 
        for word in text:
            self.vocab.add(word)
            #Maintain queue of n most recent words
            previous.append(word)
            if len(previous) < n:
                continue
            self.total_grams += 1
            while len(previous) > n:
                previous.pop(0)
            # Updating the occurence counts
            key = str(previous)
            if key in self.dictionary:
                self.dictionary[key] += 1
            else:
                self.dictionary[key] = 1
                unique_ngrams += 1

            # Keeping track of counts for low-frequency words
            if (self.smoothing_bound > 0):
                count = self.dictionary[key]
                if count > 1 and count <= (self.smoothing_bound+1):
                    self.count_list[count-1] -= 1
                if count <= self.smoothing_bound:
                    self.count_list[count] += 1

        self.unique_words = len(self.vocab)
        self.count_list[0] = self.unique_words**n - unique_ngrams
        #print("Current Model Completed.")
        if (self.smoothing_bound > 0):
            self.apply_smoothing()

    #Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
    #We might have to iterate over the whole dictionary. Yuck.
    #Optimization could be to iterate before we fill with zeros - the dict will be much smaller
    def apply_smoothing(self):
        for k in self.dictionary.keys():
            count = self.dictionary[k]
            if count < self.smoothing_bound:
                self.dictionary[k] = (count + 1) * (float(self.count_list[count+1]) / float(self.count_list[count]))

    #text: regular text
    #model: the n-gram model of choice
    #n: the n in n-gram
    #output: a score proportional to the probability of text coming from this model
    #The ngram model should have some smoothing, otherwise sentences with unknown ngrams will have infinite perplexity
    def get_perplexity(self, text):
        p = 1.0
        lst = list()
        length = 0
        for word in text:
            length += 1
            #Maintain queue of n most recent tokens
            lst.append(word) 
            if len(lst) < self.n:
                continue
            while len(lst) > self.n:
                lst.pop(0)
            key = str(lst)
            #Need to smooth for unseen ngrams
            if self.smoothing_bound > 0:
                zero_count = float(self.count_list[1]) / float(self.count_list[0])
            else:
                zero_count = 0

            denominator = 0.
            numerator = 0.
            #look up difference between total grams and unique words
            if not (key in self.dictionary):
                denominator = zero_count
                numerator = self.total_grams + (zero_count * self.count_list[0])
            else:
                denominator = self.dictionary[key]
                numerator += self.dictionary[key]
                numerator += float(self.unique_words) * zero_count
            #If the denominator is 0, then a ngram was encountered exactly zero times. 
            #This won't happen with smoothing enabled.
            #If it does happen, then the sequence has infinite perplexity
            if denominator == 0:
                return float("inf")
            #Need to use logs or else we'll have some major underflow
            p += math.log10(numerator / denominator)
        return 10**(p * (1. / float(length)))   

    def get_count(self, gram):
        gram = str(gram)
        if gram in self.dictionary:
            return self.dictionary[gram]
        else:
            return 0