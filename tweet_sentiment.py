## Lab 2 - Problem 2: Derive the sentiment of each tweet
# This part oif the lab adds all the sentiment scores up for the words in the tweets,
# rates them and prints it out.  positive scores indicate the positive tweets and the
# negative correspond to negative tweets.

# $python tweet_sentiment.py AFINN-111.txt data.json

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
    score = 0
    # Remove the apostrophes in words
    words = re.sub('[^a-zA-Z\\- ]', '', tweet).split()
    # check each word and add the score up
    for word in words: 
        score += scores.get(word, 0) 
    # check tweet phrases
    for phrase in words_dict2:
        if phrase in tweet:
            score += words_dict2.get(phrase, 0)
    return score 


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
scores = {} # initialize an empty dictionary
for line in afinn:
    # break on the tabs
    term, score = line.split("\t") 
    # remove '
    term = re.sub('[^a-zA-Z\\- ]', '', term) 
    # Cast string from file to an integer
    scores[term] = int(score)

words_dict2 = getwords_dict2(scores)

save_file = open('gao_output_2020_tweet_sentiment.txt', 'a')

# To parse output 
jsonTweet = open(sys.argv[2])
tweet_num = 1
for line in jsonTweet: 
    if line.startswith("{"):
        finalOutput = json.loads(line)
        if 'text' in finalOutput.keys():# get tweet 
            print("Score: {}".format(sentiment(scores, words_dict2, finalOutput["text"])))
            print_output = "Tweet Number {} score: {}\n".format(tweet_num, sentiment(scores, words_dict2, finalOutput["text"]))
            save_file.write(print_output)
            tweet_num += 1