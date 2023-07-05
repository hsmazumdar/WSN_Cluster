# ClusterHsm.py
# *********************************************
# *       A new Clustering Algorithm          *
# *                  by                       *
# *	         Himanshu Mazumdar                *
# *	       Date:- 31-August-2022              *
# *********************************************
import math
import random
from random import randint
import subprocess

# *********************************************
distmarix = []
nodes = []
nodGrp = []


# *********************************************
def GetRandomNodes(nods, gapx, wdt, gapy, hgt):
    arr1 = []
    for val in range(nods):
        col1 = []
        point = [
            random.randrange(gapx, wdt),
            random.randrange(gapy, hgt),
        ]
        col1.append(point[0])  # x
        col1.append(point[1])  # y
        col1.append(val)  # sno
        col1.append(0)  # grpno
        arr1.append(col1)
    arr1.sort()
    global nodes
    nodes = []
    for val in range(nods):
        col2 = []
        col2.append(val)  # new sno
        col2.append(arr1[val][0])  # x
        col2.append(arr1[val][1])  # y
        col2.append(arr1[val][3])  # grpno
        nodes.append(col2)
    brk = 123


# *********************************************
def GetDistanceMatrix(nodes):
    global distmarix
    distmarix = []
    for n1 in range(len(nodes)):
        d1x = nodes[n1][1]
        d1y = nodes[n1][2]
        dstmtx = []
        for n2 in range(len(nodes)):
            d2x = nodes[n2][1]
            d2y = nodes[n2][2]
            dst = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
            g2 = []
            g2.append(dst)
            g2.append(n2)
            dstmtx.append(g2)
        dstmtx.sort()
        distmarix.append(dstmtx)
    a = 123


# *********************************************
def GetClusterArray():
    global nodes
    GetDistanceMatrix(nodes)
    for ng in range(len(nodes)):  # reset old group numbers
        nodes[ng][3] = 0
    nodno = randint(0, len(nodes) - 1)  # get a random node
    nodno = GetFurthestNode(nodno)  # get the Furthest Node
    nodno = GetFurthestNode(nodno)  # get the Furthest Node again
    nomx = len(nodes)
    ngptr = 0
    while True:
        nodno = GetFurthestNode(nodno)  # get the Furthest Node again
        nodes[nodno][3] = nomx  # furthest node marked with nomx (a highest number)
        for n1 in range(nodGrp[ngptr] - 1):  # one less for first furthest node
            nodmn = GetNearestNode(nodno)  # get the Neareest Nodes of Furthest nod
            nodes[nodmn][3] = nomx
            grphd = GetGroupHead(nomx)
            nodno = grphd
            a = 123
        ngptr = ngptr + 1
        for n1 in range(len(nodes)):  # one less for first furthest node
            if nodes[n1][3] == nomx:
                nodes[n1][3] = grphd
        if ngptr >= len(nodGrp):
            break
    page = ""
    for n1 in range(len(nodes)):  #
        page += (
            str(nodes[n1][0])
            + ","
            + str(nodes[n1][1])
            + ","
            + str(nodes[n1][2])
            + ","
            + str(nodes[n1][3])
            + "\n"
        )
        # print(nodes[n1][0],nodes[n1][1],nodes[n1][2],nodes[n1][3])
    file1 = open("wsnHsm.csv", "w")
    file1.writelines(page)
    file1.close()
    brk = 123


# *********************************************
def GetFurthestNode(nodno):
    global distmarix
    global nodes
    pn = len(distmarix[nodno]) - 1
    while True:
        d2 = distmarix[nodno][pn]
        n2 = d2[1]
        if nodes[n2][3] == 0:
            break
        pn = pn - 1
        if pn <= 0:
            break
    return n2


# *********************************************
def GetNearestNode(nodno):
    global distmarix
    pnmx = len(distmarix[nodno]) - 1
    pn = 1  # pn = 0 is self distance and always 0
    while True:
        d2 = distmarix[nodno][pn]
        n2 = d2[1]
        if nodes[n2][3] == 0:
            break
        pn = pn + 1
        if pn >= pnmx:
            break
    return n2


# *********************************************
def GetGroupHead(nomx):
    grpmem = []
    for i in range(len(nodes)):
        if nodes[i][3] == nomx:
            grpmem.append(i)
    buf1 = []
    for i in range(len(grpmem)):
        d1x = nodes[grpmem[i]][1]
        d1y = nodes[grpmem[i]][2]
        buf2 = []
        sum = 0
        for j in range(len(grpmem)):
            d2x = nodes[grpmem[j]][1]
            d2y = nodes[grpmem[j]][2]
            dst = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
            sum += dst
        buf2.append(sum)
        buf2.append(grpmem[i])
        buf1.append(buf2)
    buf1.sort()
    gh = buf1[0][1]
    return gh
    a = 123


# *********************************************
def getGoodness():
    al = []
    for i in range(len(nodes)):
        if nodes[i].grpId == i:
            al.append(i)
    sum = 0
    for i in range(len(al)):
        clhd = int(al[i])
        for j in range(len(nodes)):
            if nodes[j].grpId == clhd:
                sum += distance(clhd, j)  # New Added
    return sum


# *********************************************
def distance(p1, p2):
    return math.sqrt(
        (p1[1] - p2[1]) * (p1[1] - p2[1]) + (p1[2] - p2[2]) * (p1[2] - p2[2])
    )


# *********************************************
def make_nodGrp(nds, grs):
    global nodGrp
    nods = int(nds)
    grps = int(grs)
    nodGrp = []
    if grs == "":
        grps = int(math.sqrt(nds) + 0.5)
    stp = float(nods) / grps
    sum = 0
    for i in range(grps):
        sum += stp
        nodGrp.append(int(sum + 0.5))
        sum -= int(nodGrp[i])
    a = 123
    return nodGrp


# Populate my nearest mynodes **********************************
def populate_mynodes(txrange):
    global nodes, srcno, dstno, mynodes
    mynodes = []
    for i in range(len(nodes)):
        buf1 = []
        for j in range(len(nodes)):
            if i != j:
                buf2 = []
                d = distance_n1_n2(i, j)
                buf2.append(d)
                buf2.append(j)
                buf1.append(buf2)
        buf1.sort()
        mynds = []
        for k in range(len(buf1)):
            if buf1[k][0] <= txrange:
                mynds.append(buf1[k][1])
        mynodes.append(mynds)
    a = 123


# get distance between n1,n2 ***********************************
def distance_n1_n2(n1, n2):
    d1x = nodes[n1][1]
    d1y = nodes[n1][2]
    d2x = nodes[n2][1]
    d2y = nodes[n2][2]
    dst2 = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
    dst2 = round(dst2, 2)
    return dst2


# *********************************************
