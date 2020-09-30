# Lab 1 - Problem 4 - Compute Term Frequency
# The goal of this script is to determine the frequency of words in tweets


import sys
import json
import re 

def lines(fp):
    print (str(len(fp.readlines())))

def main():
    sent_file = open(sys.argv[0])
    filename = open(sys.argv[1]) # added for <tweet_file> ***
    

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


# Function initializes a new dictionary, with all the words in it, to have values of zero 
def initialize_count(scores): 
    """
    This functuon makes a new dictionary with all words and then sets all counts to 0

    :param scores: dictionary of words that we want to add to the new dicitionary
    """
    countDict = {}
    for word in scores: 
        countDict[word] = 0
    return countDict
           
# Function adds words to dictionary 
def addWords(initWords, tweet):
    tweet = tweet.lower()
    ## When loading in dictionary remove all apostraphes. 
    words = re.sub('[^a-zA-Z\\- ]', '', tweet).split()
    for word in words: 
        if word not in initWords: # if word not there add it and add 1 to count value
            initWords[word] = 1
        else : # if word already there increment its value 
            initWords[word] += 1
    return initWords

#Function calculates the frequency of each word
def getFreq(countDict): 
    """
    This function calculates the frequency of each word

    :param countDict: count of the words seen

    returns countDict: updated version with the frequency counted
    """
    total = len(countDict) 
    for word in countDict: 
        countDict[word] = countDict[word] / total 
    return countDict
    

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

# calculate number of tweets 
for x in jsonTweet: 
    if x.startswith("{"):
        finalOutput = json.loads(x)
        if 'text' in finalOutput.keys():
            count += 1
            
initWords = initialize_count(scores) # makes all of the count # equal to zero
jsonTweet.seek(0) # start at begining of file again


for line in jsonTweet: 
    if line.startswith("{"):
        finalOutput = json.loads(line)
        if 'text' in finalOutput.keys():
            calcScores.append(sentiment(scores, words_dict2, finalOutput["text"]))
            index = len(calcScores)
            finalWords = addWords(initWords, finalOutput["text"])
finalDict = getFreq(finalWords)

save_file = open('gao_output_2020_frequency.txt', 'a')
#print the data to console
for k in finalDict.keys():
    print_output = ("{}\t{}".format(k, finalDict[k]))
    print(print_output)
    save_file.write(print_output)
    save_file.write("\n")