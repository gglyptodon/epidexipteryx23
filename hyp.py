import pyphen
import random
import pickle 
from bs4 import BeautifulSoup
from twython import Twython
import json
import urllib2


def getHaikuLine(num, syldct):
    #qnd
    MX = 10
    resList = []
    tmp = syldct.copy()
    res = ""
    while (num >0 and MX >0 ):
        MX -=1
        keys = [k for k in tmp.keys() if k <= num]
        rk = random.choice(keys)
        numback = num
        num = num-rk
        while num <0 :
            MX -=1
            num = numback
            rk = random.choice(keys)
            numback = num
            num = num-rk
        wrd = random.choice(tmp[rk])
        wrd = wrd.replace('"','')
        res += wrd.strip()+" "
    return(res+"\n")


def main():
    pyphen.language_fallback('en_EN')
    d = pyphen.Pyphen(lang='de_DE')
    res = d.inserted('internet')
    with open("index.html",'r') as m:
        markup = m.read()
    bs = BeautifulSoup(markup, "html.parser")
    resources = bs.find_all('h2')
    resclean = []
    for r in resources:
        bl = r.find_all('img')
        tmp = [b for b in r if b not in bl]
        resclean += tmp

    #5,7,5
    syll = {}
    tmp = [r.split( ) for r in resclean]
    resclean = []
    for t in tmp:
        resclean +=t
    
    for r in resclean:
        r = r.strip()
        tmp = d.inserted(r)
        if tmp.startswith("-"):
            tmp = tmp[1:]
        l = (len(tmp.split("-")))
        try:
            syll[l].append(tmp)
        except KeyError as k:
            syll[l] = [tmp]
    haiku = False
    while haiku is False:
        lineOne = getHaikuLine(5, syll)
        lineTwo = getHaikuLine(7, syll)
        lineThree = getHaikuLine(5,syll)
        haiku = True

    tweet = "".join([lineOne,lineTwo,lineThree])
    
    crd = pickle.load(open("crd.nope",'r'))
    api = Twython(crd["apiKey"],crd["apiSecret"],crd["accessToken"],crd["accessTokenSecret"])
    ok = False
    while (ok == False):
       if len(tweet) <= 140:
           ok = True
           api.update_status(status=tweet)
           print("tweet: " + tweet)


if __name__ == "__main__":
    main()
