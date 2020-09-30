# Lab 1 - Part 5 - which state is happiest? 
# The goal of this script is to identify the happiest state

import sys
import json
import re 

def lines(fp):
    print (str(len(fp.readlines())))

def main():
    sent_file = open(sys.argv[0])
    filename = open(sys.argv[1]) # added for <tweet_file> ***
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
    
# Dictionary of states and their abbriviations 
statesAbbrev = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas', 'AZ': 'Arizona','CA': 'California',
          'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware','FL': 'Florida', 'GA': 'Georgia',
          'HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas',
          'KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine',
          'MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MS': 'Mississippi','MT': 'Montana',
          'NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire',
          'NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio',
          'OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','RI': 'Rhode Island','SC': 'South Carolina',
          'SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VT': 'Vermont',
          'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia','WY': 'Wyoming'}

calcScores = []  
# Create a dictionary of the states and their sentiment values 
stateSentiment = {}

afinn = open(sys.argv[1])
scores = {}
for line in afinn:
    term, score = line.split("\t")
    term = re.sub('[^a-zA-Z\\- ]', '', term) 
    scores[term] = int(score)
words_dict2 = getwords_dict2(scores) 


# To parse output 
jsonTweet = open(sys.argv[2])
for line in jsonTweet: 
    if line.startswith("{"):
        finalOutput = json.loads(line)
        if 'text' in finalOutput.keys():
            tweetSentiment = (sentiment(scores, words_dict2, finalOutput["text"]))
            if 'place' in finalOutput.keys() and finalOutput['place'] is not None:
                if finalOutput['place']['country_code'] == 'US':
                    fullName = finalOutput['place']['full_name']
                    state = fullName.split(" ")[-1]
                    stateFull = fullName.rsplit(', ', 1)[0]
                    if (len(state) == 2) and (state in statesAbbrev):
                        if state in stateSentiment :
                            stateSentiment[state] += tweetSentiment
                        else: 
                            stateSentiment[state] = tweetSentiment
                    elif (len(state) == 3) and (state == "USA"): 
                        for x in statesAbbrev:
                            if statesAbbrev[x] == stateFull:
                                if state in stateSentiment :
                                    stateSentiment[x] += tweetSentiment
                                else: 
                                    stateSentiment[x] = tweetSentiment

# go through list of states to find happiest state
save_file = open('gao_output_2020_happiest_state.txt', 'a')

happiestState = ''
happiestValue = 0; 
for temp_happy_state in stateSentiment: 
    print_output = ("{}\t{}\n".format(temp_happy_state, stateSentiment[temp_happy_state]))
    save_file.write(print_output)
    if stateSentiment[temp_happy_state] >= happiestValue: 
        happiestValue = stateSentiment[temp_happy_state]
        happiestState = temp_happy_state


# print out happiest state 
print(happiestState, happiestValue)

