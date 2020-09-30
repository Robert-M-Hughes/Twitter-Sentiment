# Lab 1 - Problem 3: Derive the sentimen of new terms 
# The goal of this is to add words to the sentiment that we dont already have scores for

# $python term_sentiment.py AFINN-111.txt data.json

import sys
import json
import re 

def lines(fp):
    print (str(len(fp.readlines())))

def main():
    sent_file = open(sys.argv[0])
    file1 = open(sys.argv[1])
    file2 = open(sys.argv[2])


def sentiment(scores, words_dict2, tweet):
    tweet = tweet.lower()
    """
    This function calculates the sentiment od the tweets by going through the dictionary
    and then returns the updated dictionary

    :param words_dict2: dictionary of the words we want to compare with
    :param tweet: Tweet we want to derive the sentiment of

    :returns score:  The score of the tweet.
    """
    ## Remove the apostrophes in words
    words = re.sub('[^a-zA-Z\\- ]', '', tweet).split()
    score = 0
    # check each word and add the score up
    for word in words: 
        score += scores.get(word, 0) 
    # check tweet phrases
    for phrase in words_dict2:
        if phrase in tweet:
            score += words_dict2.get(phrase, 0)
    return score
           

def addWords(scores, tweet, tweetValue, count):
    """
    This function adds new words to the dictionary from words found in the tweets.

    :param tweet: tweet that we are looking at to determine if there are new words
    :param tweetValue: sentiment of the tweet given by sentiment function
    :param count: total number of words in the file

    :returns scores:  updated scores of dictionary
    """
    tweet = tweet.lower() 
    words = re.sub('[^a-zA-Z\\- ]', '', tweet).split()
    for word in words: 
        if word not in scores:
            value = tweetValue/count 
            scores[word] = value
        else:
            scores[word] += tweetValue/count
    return scores


def sortScores(scores): 
    """
    This function is to reorder the scores from low to high so they are in order

    :param scores: dictionary of the new scores that we want to sort.

    :returns sortedScores:  dictionary of the sorted scores
    """
    sortedScores = sorted(scores.items(), key=lambda kv: kv[1])
    return sortedScores
    

def getwords_dict2(scores):
    """
    This function takes the words that have spaces in them ('dont like') and add them to a dictionary and check for words in the string

    :param scores: dictionary of the scores to compute
    """
    words_dict2 = {}
    for word in scores:
        if ' ' in word: 
            words_dict2[word] = scores.get(word)
    return words_dict2
    
  
if __name__== "__main__":
    main()
    
afinn = open(sys.argv[1])
scores = {}
for line in afinn:
    term, score = line.split("\t")
    term = re.sub('[^a-zA-Z\\- ]', '', term) 
    scores[term] = int(score)
words_dict2 = getwords_dict2(scores) 

# To parse output 
calcScores = []
count = 0

jsonTweet = open(sys.argv[2])

for x in jsonTweet: 
    if x.startswith("{"):
        finalOutput = json.loads(x)
        if 'text' in finalOutput.keys():
            tweet = finalOutput['text'].lower()
            # need to remove the apostrophes
            words = re.sub('[^a-zA-Z\\- ]', '', tweet).split()
            # get the total words
            for word in words:
                count += 1

jsonTweet.seek(0) 

for line in jsonTweet: 
    if line.startswith("{"):
        finalOutput = json.loads(line)
        if 'text' in finalOutput.keys():
            calcScores.append(sentiment(scores, words_dict2, finalOutput["text"])) 
            index = len(calcScores) - 1 
            addWords(scores, finalOutput["text"], calcScores[index], count) 

sortedScores = sortScores(scores)
save_file = open('gao_output_2020_term_sentiment.txt', 'a')
finalDict = sortedScores
#print the data to console
for k in finalDict:
    word, score = k
    print_output = "{}\t{}".format(word, score)
    print(print_output)
    save_file.write(print_output)
    save_file.write("\n")

