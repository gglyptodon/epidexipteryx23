import sys
import json
import pickle
from markovchain import MarkovChain
import urllib2
import getopt
import random

def searchRecipes(searchterms = None, crd = None):
    recipeNames = []
    if crd is None:
        pass
    else:
        if searchterms is None:
            searchterms = ["fish", "chocolate"]
        search = "&q=".join(searchterms)
        url = "http://api.yummly.com/v1/api/recipes?_app_id="+crd["apiID"]+"&_app_key="+crd["apiKey"]+"&q="+search
        print(url)
        resp = urllib2.urlopen(url).read()
        s = json.loads(resp)
        for i in range(0, len(s["matches"])):
                recipeNames.append(s["matches"][i]["id"])
    return(recipeNames)

def returnIngredients(recipeName = None, crd = None):
    allIngredients = []
    if crd is None:
        pass
    else:
        url = "http://api.yummly.com/v1/api/recipe/"+recipeName+"?_app_id="+crd["apiID"]+"&_app_key="+crd["apiKey"]
        resp = urllib2.urlopen(url).read()
        s = json.loads(resp)
        allIngredients.append(" ".join(s["ingredientLines"]))
    return(allIngredients)

def usage():
    m = """
    usage: -o OUT -s SEARCHTERMS (eg "xyz bla")
    """

def main():
    crd = pickle.load(open("./crdy.nope",'r'))
    outfile = None
    outdebug = None
    searchterms = ["strawberries","gorgonzola"] 
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "o:s:h", ["out=","search=","help"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()
    for o, a in opts:
        if o in ("-o", "--out"):
            outfile = a
            autdebug = a+".debug"
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-s", "--search"):
            searchterms = a.split(" ")
        else:
            assert False, "unhandled option"
    
    if outfile is None:
        outfile = "out.tmp"
        outdebug = outfile+".debug"


    rec = searchRecipes(crd=crd, searchterms = searchterms)
    #print(rec)
    corpus = []
    randomRec = set()
    for i in range(0,5):
        randomRec.add(random.choice(rec))
     
    with open(outdebug,'w') as o:
        for r in randomRec:
            print(r,"RR")
            o.write(r)
            o.write("\n")
            ing = returnIngredients(recipeName = r, crd = crd)
            print("ing", r, returnIngredients(recipeName = r, crd = crd))
            corpus += ing
    
    corpus = [c.encode('utf-8') for c in corpus]
    jc = " ".join(corpus)
    jc = jc.replace("\n"," ")
    with open(outdebug, 'w') as o:
        o.write("***".join(corpus))
        o.write("\n")
        o.write(jc)
    
    mc = MarkovChain(corpus = jc, separator = " ")
    result = mc.printSth(2000)
    with open(outfile, 'w') as o:
        o.write(result)
if __name__=="__main__":
    main()
