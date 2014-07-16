import random;
import sys;


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


def main():
    mc = MarkovChain(corpus = open(sys.argv[1],'r').read(), separator = " ")
    #print(mc.chain)
    print(mc.printSth(int(sys.argv[2])))
if __name__ == "__main__":
    main()
