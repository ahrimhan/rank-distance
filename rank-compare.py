import os
import sys
from pprint import pprint
import csv
import math

CURDIR = os.path.abspath(os.path.dirname(__file__))

class ARRank:
    rankToEntry = []
    entryToRank = {}
    entryToAttr = {}

    def __init__(self):
        self.rankToEntry = []
        self.entryToRank = {}
        self.entryToAttr = {}
    def load(self, filename, count):
        raw_data = open(filename)
        reader = csv.reader(raw_data, skipinitialspace=True, delimiter=',', quotechar='"')
        i = 0
        entry_len = 0
        for entry_data in reader:
            entry_len = entry_len + 1
            if count != 0 and count <= i:
                continue
            self.entryToAttr[entry_data[0]] = entry_data[1:]
            self.rankToEntry.append(entry_data[0])
            self.entryToRank[entry_data[0]] = i
            i = i + 1
        raw_data.close()
        return entry_len
    def entrySet(self):
        return set(self.rankToEntry)

    def unionEntrySet(self, otherRank):
        return self.entrySet().union(otherRank.entrySet())

    def minusEntrySet(self, otherRank):
        return self.entrySet().difference(otherRank.entrySet())
        

class KendallsTau:
    p = 0.0
    def __init__(self, p):
        self.p = p
    def rankDistance(self, rankA, rankB):
        unionSet = rankA.unionEntrySet(rankB)
        unionList = list(unionSet)
        unionUnorderedPairSet = set()
        for i in range(len(unionSet)-1):
            for j in range(i+1, len(unionSet)):
                unionUnorderedPairSet.add((unionList[i], unionList[j]))
        k = 0.0
        for (i, j) in unionUnorderedPairSet:
#case 1
            if i in rankA.entrySet() and j in rankA.entrySet() and i in rankB.entrySet() and j in rankB.entrySet():
                if (rankA.entryToRank[i] < rankA.entryToRank[j]) and (rankB.entryToRank[i] < rankB.entryToRank[j]):
                    pass
                elif (rankA.entryToRank[i] > rankA.entryToRank[j]) and (rankB.entryToRank[i] > rankB.entryToRank[j]):
                    pass
                else:
                    k = k + 1
#case 2
            elif i in rankA.entrySet() and j in rankA.entrySet() and i in rankB.entrySet():
                if rankA.entryToRank[i] < rankA.entryToRank[j]:
                    pass
                elif rankA.entryToRank[i] > rankA.entryToRank[j]:
                    k = k + 1
            elif i in rankA.entrySet() and j in rankA.entrySet() and j in rankB.entrySet():
                if rankA.entryToRank[i] < rankA.entryToRank[j]:
                    k = k + 1
                elif rankA.entryToRank[i] > rankA.entryToRank[j]:
                    pass
            elif i in rankA.entrySet() and i in rankB.entrySet() and j in rankB.entrySet():
                if rankB.entryToRank[i] < rankB.entryToRank[j]:
                    pass
                elif rankB.entryToRank[i] > rankB.entryToRank[j]:
                    k = k + 1
            elif j in rankA.entrySet() and i in rankB.entrySet() and j in rankB.entrySet():
                if rankB.entryToRank[i] < rankB.entryToRank[j]:
                    k = k + 1
                elif rankB.entryToRank[i] > rankB.entryToRank[j]:
                    pass
#case 4
            elif i in rankA.entrySet() and j in rankA.entrySet():
                k = k + self.p
            elif i in rankB.entrySet() and j in rankB.entrySet():
                k = k + self.p
#case 3
            elif i in rankA.entrySet() and j in rankB.entrySet():
                k = k + 1
            elif j in rankA.entrySet() and i in rankB.entrySet():
                k = k + 1
            else:
                pass
        return k

class SpearmansFootrule:
    def rankDistance(self, rankA, rankB):
        return self.genericRankDistance(rankA, rankB, 0)

    def genericRankDistance(self, rankA, rankB, l):
        unionSet = rankA.unionEntrySet(rankB)
        if l == 0:
            l = ((len(rankA.entrySet()) + len(rankB.entrySet()))/2.0 * 3.0 - len(unionSet) + 1.0)/2.0

        f = 0.0
        for i in unionSet:
            if i in rankA.entrySet():
                tA = float(rankA.entryToRank[i])
            else:
                tA = l

            if i in rankB.entrySet():
                tB = float(rankB.entryToRank[i])
            else:
                tB = l

            if tA > tB:
                t = tA - tB
            else:
                t = tB - tA
            f = f + t
        return f



def main():
    if len(sys.argv) != 5:
        print "Usage: %s [category] [static-cutline] [dynamic-cutline] [changed-cutline]" % sys.argv[0]
        sys.exit(1)

    try:
        rankfile1 = sys.argv[1] + "-static.dat"
        rankfile2 = sys.argv[1] + "-dynamic.dat"
        rankfile3 = sys.argv[1] + "-changed.dat"
        rankN1 = int(sys.argv[2])
        rankN2 = int(sys.argv[3])
        rankN3 = int(sys.argv[4])
    except Exception:
        print "Usage: %s [category] [static-cutline] [dynamic-cutline] [changed-cutline]" % sys.argv[0]
        sys.exit(1)

    rankfullfile1 = os.path.join(CURDIR, rankfile1)
    rankfullfile2 = os.path.join(CURDIR, rankfile2)
    rankfullfile3 = os.path.join(CURDIR, rankfile3)
    rank1 = ARRank()
    rank2 = ARRank()
    rank3 = ARRank()
    rt1 = rank1.load(rankfullfile1, rankN1)
    rt2 = rank2.load(rankfullfile2, rankN2)
    rt3 = rank3.load(rankfullfile3, rankN3)

    kt = KendallsTau(0.5)
    static_k = kt.rankDistance(rank1, rank3)
    sf = SpearmansFootrule()
    static_f = sf.rankDistance(rank1, rank3)

    kt = KendallsTau(0.5)
    dynamic_k = kt.rankDistance(rank2, rank3)
    sf = SpearmansFootrule()
    dynamic_f = sf.rankDistance(rank2, rank3)

    if rankN1 == 0:
        rankN1 = rt1
    if rankN2 == 0:
        rankN2 = rt2
    if rankN3 == 0:
        rankN3 = rt3

    rf1 = float(rankN1) / rt1 * 100
    rf2 = float(rankN2) / rt2 * 100
    rf3 = float(rankN3) / rt3 * 100

    print "static:%3d/%3d(%7.2f%%) dynamic:%3d/%3d(%7.2f%%) changed:%3d/%3d(%7.2f%%) | Static K:%9.2f F:%9.2f | Dynamic K:%9.2f F:%9.2f" % (rankN1, rt1, rf1, rankN2, rt2, rf2, rankN3, rt3, rf3,static_k, static_f, dynamic_k, dynamic_f)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Terminating program..."
