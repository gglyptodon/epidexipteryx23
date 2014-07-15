import pickle
from bs4 import BeautifulSoup
from twython import Twython
import urllib2
import re
import time
def grabSite(url ='http://www.studentenwerk-duesseldorf.de/Essen/Speiseplan.php?ort=3.500'):
    resp = urllib2.urlopen(url).read()
    return(resp)

class Food():
    def __init__(self,name, info, price):
        self.name = name
        self.info = info
        self.price = price
    def __repr__(self):
        return(self.name+" "+self.price)
    def isGF(self):
        if "20" in self.info:
            return False
        else:
            return True


#def grabSite():
#    return(open("essen.html",'r').read())

def tweetInPieces(longtweet,api):
    print(len(longtweet))
    if len(longtweet) > 140:
        t1 = longtweet[0:139]
        print(t1)
        #api.update_status(status=t1)
        longtweet = longtweet[139:]
        time.sleep(10)
        tweetInPieces(longtweet, api)
    else:
        print(longtweet)
        #api.update_status(status=longtweet)


def main():
    markup = grabSite()
    bs = BeautifulSoup(markup, "html.parser")
    resources = bs.find_all("div",{"id": "day0"})
    todaysGFFood = []
    eintopf = []
    costs =  bs.find_all("div",{"id":"essen-study"})
    costs = [c for c in costs if not "0,00" in c.p.string.encode('utf-8')]
    f = lambda x:[y.p for y in x]
   # print(f(costs))
    for r in resources:
        tmpp = [x.p for x in r.find_all("div",{"id": "essen-text"}) if x.br ]
        tmpbr = [x.br for x in r.find_all("div",{"id": "essen-text"}, text = True) ]
        for i,j in enumerate(tmpp):
            info = str(j.br)
            info = re.sub("<br>","", info)
            info = re.sub("</br>","",info)
            j = str(j)
            wrds = j.split(" ")
            wrds = ["".join(w.split()) for w in wrds]
            j = " ".join(wrds)
            j = j.replace("<p>","")
            j = j.replace("</p","")
            j = re.sub('<br.*','',j)
            name = j
            try:
                food = Food(name = name, info = info, price = str(costs[i].p.string.encode('utf-8').replace("Studenten:","").strip()))
            except UnicodeEncodeError as e:
                print(e)
                food = Food(name = name, info = info, price = str(costs[i].p))
            if "Weizenbr" in name:
                eintopf.append(food)
            if food.isGF():
                todaysGFFood.append(food)
    f = lambda x: [str(y) for y in x ]
    tweet =""
    if len(todaysGFFood) == 0:
        tweet = "nothing gluten free today\n"
    else:
        tweet = "gluten free: "+"\n".join(f(todaysGFFood))+"\n"
    if eintopf:
        tweet+="soup: "+str(eintopf[0])
    #print(tweet)
    crd = pickle.load(open("crd.nope",'r'))
    api = Twython(crd["apiKey"],crd["apiSecret"],crd["accessToken"],crd["accessTokenSecret"])
    tweetInPieces(tweet,api)


if __name__ == "__main__":
    main()
