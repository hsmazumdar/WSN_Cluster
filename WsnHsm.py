# WsnHsm.py
# *********************************************
# *   Wireless Sensor Network Simulation      *
# *                  by                       *
# *	         Himanshu Mazumdar                *
# *	       Date:- 31-August-2022              *
# *********************************************
import tkinter as tk
from tkinter import Canvas
from tkinter import *
import math
import random
from random import randint
import subprocess
import ClusterHsm as clst
# *********************************************
# *********************************************
def draw_nodes():
    canvas.delete('all')
    nds = widgetIn2.get(1.0, "end-1c")
    grs = grptxt.get(1.0, "end-1c")
    nods=int(nds)
    clst.GetRandomNodes(nods, 10, wdt-30, 10, hgt-120)
    for val in range(len(clst.nodes)):
        canvas.create_oval(clst.nodes[val][1], clst.nodes[val][2], clst.nodes[val][1]+20, clst.nodes[val][2]+20, 
                        fill='white', outline='red')  
        canvas.create_text(clst.nodes[val][1] + 10, clst.nodes[val][2] + 10, text=str(clst.nodes[val][0]),
                            fill="red", font=('Helvetica 10 bold'))
    canvas.pack()                
    a = 123
    # subprocess.call('WsnHsmUtils.exe wsnHsm.txt')
# *********************************************
def draw_wsn():
    canvas.delete('all')
    dist = 0
    for val in range(len(clst.nodes)):
        n1 = clst.nodes[val][3]
        x1 = clst.nodes[val][1]+10
        y1 = clst.nodes[val][2]+10
        x2 = clst.nodes[n1][1]+10
        y2 = clst.nodes[n1][2]+10
        canvas.create_line(x1, y1, x2, y2, width=3, fill='green')  #draw line
        dist += math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    lbl5.config(text=str(int(dist)))    
    for val in range(len(clst.nodes)):
        canvas.create_oval(clst.nodes[val][1], clst.nodes[val][2], clst.nodes[val][1]+20, clst.nodes[val][2]+20, 
                        fill='white', outline='red')  #draw nodes
        canvas.create_text(clst.nodes[val][1] + 10, clst.nodes[val][2] + 10, text=str(clst.nodes[val][0]),
                        fill="red", font=('Helvetica 10 bold')) #draw nodes number
    canvas.pack()                
# *********************************************
def redraw_nodes():
    canvas.delete('all')
    for val in range(len(clst.nodes)):
        canvas.create_oval(clst.nodes[val][1], clst.nodes[val][2], clst.nodes[val][1]+20, clst.nodes[val][2]+20, 
                        fill='white', outline='red')  #draw nodes
        canvas.create_text(clst.nodes[val][1] + 10, clst.nodes[val][2] + 10, text=str(clst.nodes[val][0]),
                        fill="red", font=('Helvetica 10 bold')) #draw nodes number
    canvas.pack()                
# *********************************************
def draw_grps() :
    nds = widgetIn2.get(1.0, "end-1c")  #input number of nodes
    grs = grptxt.get(1.0, "end-1c")     #input number of clusters
    nodGrp = clst.make_nodGrp(nds, grs) #number of nodes per cluster
    clst.GetClusterArray()              #main clustering algorithm
    draw_wsn()
    a=123
# *********************************************
def optimize_grps() : 
    global dstMx   
    count = 0
    for i in range(len(clst.nodes)) :
        d1x = clst.nodes[i][1]
        d1y = clst.nodes[i][2]
        ghi = clst.nodes[i][3]
        dstmn = dstMx
        jj = -1
        for j in range(len(clst.nodes)) :
            ghj = clst.nodes[j][3]
            if ghj == j :
                d2x = clst.nodes[j][1]
                d2y = clst.nodes[j][2]
                dst = math.sqrt((d1x-d2x)*(d1x-d2x)+(d1y-d2y)*(d1y-d2y))
                if  dstmn > dst :
                    dstmn = dst
                    jj = j
        if ghi != jj :
            clst.nodes[i][3] = jj
            count += 1
    draw_wsn()            
    a=123
# *********************************************
# Main Loop
# *********************************************
app = tk.Tk()
app.title("Canvas")
wdt= app.winfo_screenwidth()*8/10   #screen width of monitor
# wdt= app.winfo_screenwidth()        #screen width of monitor
hgt= app.winfo_screenheight()       #screen height of monitor
dstMx = math.sqrt(wdt*wdt+hgt*hgt)  #default number of clusters
app.geometry("%dx%d" % (wdt, hgt))  #setting tkinter window size
app.state('zoomed')                 #full screen display
canvas = tk.Canvas(bg="blue", width=wdt-10, height=hgt-100)
canvas.pack(anchor=tk.NW)           #set a blue canvas
widgetIn2 = tk.Text(app, height = 1, width = 5)
widgetIn2.insert(tk.END, "100") #default number of nodes
widgetIn2.pack(side=tk.LEFT)    #input number of nodes
#..............................................
widgetIn2 = tk.Text(app, height = 1, width = 5)
widgetIn2.insert(tk.END, "100") #default number of nodes
widgetIn2.pack(side=tk.LEFT)    #input number of nodes
lbl1 = tk.Label(app,text="nodes", fg="black")
lbl1.pack(side=tk.LEFT)
button1 = tk.Button(app, text="NewSet", fg="red", command=draw_nodes)
button1.pack(side=tk.LEFT)      #button to draw new set of nodes
button2 = tk.Button(app, text="ReDraw", fg="red", command=redraw_nodes)
button2.pack(side=tk.LEFT)      #button to redraw draw nodes
grptxt = tk.Text(app, height = 1, width = 5)
grptxt.insert(tk.END, "10")     #default number of clusters
grptxt.pack(side=tk.LEFT)       #input number of clusters
lbl2 = tk.Label(app,text="grps", fg="black")
lbl2.pack(side=tk.LEFT)
button3 = tk.Button(app, text="Cluster", fg="red", command=draw_grps)
button3.pack(side=tk.LEFT)      #button to do clustering
button4 = tk.Button(app, text="Optimize", fg="red", command=optimize_grps)
button4.pack(side=tk.LEFT)      #button to optimize
lbl4 = tk.Label(app,text="total path:", fg="black")
lbl4.pack(side=tk.LEFT)
lbl5 = tk.Label(app,text="0", fg="black")
lbl5.pack(side=tk.LEFT)
# lbl5.config(text="1234")
button10 = tk.Button(app, text="Exit", width=15, bg="red", command=quit)
button10.pack(side=tk.RIGHT)
app.mainloop()
# *********************************************