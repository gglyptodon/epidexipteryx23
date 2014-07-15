import pickle
from bs4 import BeautifulSoup
#from twython import Twython
import urllib2
import re

#def grabSite(url ='http://www.studentenwerk-duesseldorf.de/Essen/Speiseplan.php?ort=3.500'):
#    resp = urllib2.urlopen(url).read()
#    return(resp)

class Food():
    def __init__(self,name, info, price):
        self.name = name
        self.info = info
        self.price = price
    def __repr__(self):
        return(self.name)
    def isGF(self):
        if "20" in self.info:
            return False
        else:
            return True


def grabSite():
    return(open("essen.html",'r').read())

def main():
    markup = grabSite()
    bs = BeautifulSoup(markup, "html.parser")
    resources = bs.find_all("div",{"id": "day0"})
    todaysGFFood = []
    for r in resources:
        tmpp = [x.p for x in r.find_all("div",{"id": "essen-text"}) if x.br ]
        tmpbr = [x.br for x in r.find_all("div",{"id": "essen-text"}, text = True) ]
        for j in tmpp:
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
            food = Food(name = name, info = info, price = None)
            #print(name)
            if food.isGF():
                todaysGFFood.append(food)
                #print(food)
    f = lambda x: [str(y) for y in x ]
    #print(todaysGFFood)
    tweet = "\n".join(f(todaysGFFood))
    print(tweet)
    # crd = pickle.load(open("crd.nope",'r'))
    # api = Twython(crd["apiKey"],crd["apiSecret"],crd["accessToken"],crd["accessTokenSecret"])
    # if len(tweet) <= 140:
        #api.update_status(status=tweet)
    #   print("tweet: " + tweet)
    #print("\n".join(f(foods)))
if __name__ == "__main__":
    main()
