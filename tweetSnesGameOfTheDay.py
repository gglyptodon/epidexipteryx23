#!/usr/bin/env python
import sys
import pickle
import os
import random
from twython import Twython
import json
import urllib2
def grabGame():
    gameList = []
    with open("snesList.txt",'r') as infile:
        for l in infile:
            l = l.strip()
	    gameList.append(l)
    index = random.randint(0, len(gameList))
    return(gameList[index])

def getWiki(str):
    url = "http://en.wikipedia.org/w/api.php?action=opensearch&search="+str+"&namespace=0&format=json&suggest="
    response = urllib2.urlopen(url)
    res = json.load(response)
    print(res)
    if not res[1]:
        return(None)
    else:
        res = "_".join(res[1][0].split(" "))
        print(res)
        res = " http://en.wikipedia.org/wiki/"+res
        print(res)
        return(res)

def main():
    crd = pickle.load(open("crd.nope",'r'))
    api = Twython(crd["apiKey"],crd["apiSecret"],crd["accessToken"],crd["accessTokenSecret"])
    ok = False
    while (ok == False):
       game = grabGame()
       tweet ="Today's SNES game: "
       tweet +="{}".format(game)
       url = getWiki("%20".join(game.split(" ")))
       if url is not None:
           tweet += url
       if len(tweet) < 140:
           ok = True
           api.update_status(status=tweet)
           print("SNES game tweeted: " + tweet)

if __name__== "__main__":
    main()
