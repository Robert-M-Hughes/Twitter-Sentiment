# Lab 1 - Problem 6: Top ten hash tags
# the goal of this part of the lab is to find the top 10 hashtags

import sys
import json
import re

def lines(fp):
    print (str(len(fp.readlines())))

# Function to add words to a new dictionary containing all of the hashtags and thier frequency
def addWords(tagCount, hashtag):
    """
    Function to add hashtag to dictionary or add occurence

    :param hashtag: from the json the hastag we want to see if it appears
    :param tagCount: Dictionary of the cirrent hastags that we are tracking

    returns updated hastag dictionary
    """
    if hashtag not in tagCount: # if word not there add it and add a value
        tagCount[hashtag] = 1
    else : # if word already there increment its value
        tagCount[hashtag] += 1
    return tagCount

def reorderScores(tagCount):
    """
    Function to order hashtags by frequency

    :param tagCount: unsorted dictuonary of the hashtags
    """
    sortedHashtags = sorted(tagCount.items(), key=lambda kv: kv[1], reverse = True)
    return sortedHashtags

def main():
    sent_file = open(sys.argv[0])
    filename = open(sys.argv[1]) # added for <tweet_file> ***

if __name__== "__main__":
    main()

tagCount = {} # unordered hashtags

# To parse output
jsonOutput = open(sys.argv[2]) # opens tweet_file
# Go though file line by line
for line in jsonOutput:
    if line.startswith("{"):
        data_line = json.loads(line)
        # look for the hastags to add to the list
        if 'entities' in data_line.keys():
            hashtags = data_line['entities']['hashtags']
            for text in hashtags:
                for htext in text :
                    if htext == "text":
                        addWords(tagCount, text[htext].lower())
# sort hashtags
sortedHashtags = reorderScores(tagCount)
# count for loop
count = 0
save_file = open('gao_output_2020_top_ten.txt', 'a')
save_file.write("--------------- Top Ten ---------------\n")
# to print out the top ten hashtags
for (h, v) in sortedHashtags:
    print_output = ("{}\t{}\n".format(h, v))
    if count < 10:
        print(h, v)
    elif count == 10:
        print_output = ("--------------- End of Ten ---------------\n{}\t{}\n".format(h, v))

    count += 1
    save_file.write(print_output)
