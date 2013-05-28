import unittest
import ngram

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):        
        self.apple_gram = ngram.Ngram(2, ["apple", "ate", "an", "apple", "ate"], 1)

    #Testing the get_count function.
    #Should return the number of times a particular ngram appears in the model.
    def test_count(self):
        self.assertEqual(2, self.apple_gram.get_count(["apple", "ate"]))
        self.assertEqual(0, self.apple_gram.get_count(["apple", "asdf"]))
    
    #Testing the get_perplexity function.
    #Should return the perplexity of a sequence on a model.
    #A sequence with a lower perplexity is more similar to that model.
    #To-do: A more comprehensive test. This one is more like a sanity check.
    def test_perplexity(self):
        self.assertLess(self.apple_gram.get_perplexity(["apple", "ate", "a", "cat"]), self.apple_gram.get_perplexity(["orange", "grape", "lemon", "tomato"]))

if __name__ == '__main__':
    unittest.main()
