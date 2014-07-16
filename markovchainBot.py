import random
import sys
import urllib2
from bs4 import BeautifulSoup
import re
from twython import Twython
import pickle
class MarkovChain(object):
    def __init__(self, separator = None, corpus = None):
        self.separator = separator
        self.corpus = corpus
        self.chain = self.setChain()
    def setChain(self):
        chain = {}
        if self.separator is None:
            allItems = self.corpus.split()
        else:
            allItems = self.corpus.split(self.separator)
        mx = allItems[len(allItems)-1]
        for i,x in enumerate(allItems):
            if i == len(allItems) -1 :
                pass
            else:
                try:
                    chain[x].append(allItems[i+1])
                except KeyError as e:
                    chain[x] =[allItems[i+1]]

        try:
            chain[mx].append("\n")
        except KeyError as e:
            chain[mx] = ["\n"]
        return(chain)

    def printSth(self,maxItems = 20):
        res =""
        t = random.choice(self.chain.keys())
        for i in range(0,maxItems):
            try:
                print(self.chain[t])
                tmp = random.choice(self.chain[t])
                res += " "+tmp
                t= tmp
            except KeyError as e:
                return(res)
        return(res)


def grabNews():
    resp = urllib2.urlopen("http://spiegel.de/index.html").read()
    return(resp)

def main():

    markup = grabNews()
    bs = BeautifulSoup(markup, "html.parser")
    resources = bs.find_all('span',attrs = {"class":["headline"]} )
    print(resources)
    resclean = []
    for r in resources:
        bl = r.find_all('img')
        tmp = [b.lower() for b in r if b not in bl]
        tmp =  [re.sub('[".()]',"",b) for b in tmp]
       # for t in tmp:
        #    t = str(t.en)
        print(tmp,"tmp")
        resclean += tmp
    string = " ".join(resclean)
    mc = MarkovChain(corpus = string, separator = " ")
    print(mc.chain)
    tweet = (mc.printSth(5))
    #print(tweet)
    tweet += "\n#markovchain generated"
    print(tweet)
    crd = pickle.load(open("crd.nope",'r'))
    api = Twython(crd["apiKey"],crd["apiSecret"],crd["accessToken"],crd["accessTokenSecret"])
    #api.update_status(status = tweet)
if __name__ == "__main__":
    main()
