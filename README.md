ngram
=====

Overview
-----
Ngram models are simple yet powerful tools in the field of Natural Language Processing. An Ngram is an N-token sequence of words. For example, the sentence "natural language processing is great" has the following 2-grams (also known as bigrams):

    ["natural language", "language processing", "processing is", "is great"]


Perplexity
----
After calculating an ngram model for a body of text, one can determine the probability of a sequence of words appearing in that text. For example, one could train an ngram model on a set of legitimate emails, and train another model on a set of spam emails. Given an unknown email, one could guess whether it is spam or real by determining which model it is most likely to come from. Instead of reporting raw probabilities of sequences appearing, it is common to use perplexity, which is a function of the sequence's log probability of occurring. Sequences with lower perplexities more closely resemble the ngram model.

Smoothing
----
If a test sentence closely resembles one in the model, it should have a low perplexity. However, if that sentence contains just one ngram that was never seen in the model, it will have a probability of zero, and thus an infinite perplexity. Therefore, it is common to use a smoothing function to assign some positive probability to unseen ngrams. This program uses the Good-Turing smoothing model.

Usage Examples
----
<b>Training Ngrams</b>

    myNgram = ngram.Ngram(n, list_of_tokens, smoothingBound)
<b>n:</b> The length of each ngram (1 = unigram, 2 = bigram, etc)
<br /><b>list of tokens:</b> A training list where each element is one token in the ngram. For instance, if you wanted to generate character ngrams, you would pass in list("These are some words").
<br /><b>smoothingBound:</b> Smooths any ngram appearing below smoothingBound times in the model using Good Turing smoothing.

<b>Getting Perplexity</b>

    myNgram.getPerplexity(list_of_tokens)
    
To Do
----
+ Clean up code. All of this stuff was written under time pressure, so there are probably some hacky things in there. Also, several project-specific features were hastily removed, so there might be some unused variables and such in the present code.
