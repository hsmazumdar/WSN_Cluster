# WsnHsm.py
# *********************************************
# *   Wireless Sensor Network Simulation      *
# *                  by                       *
# *	         Himanshu Mazumdar                *
# *	       Date:- 31-August-2022              *
# *********************************************
# **************************************************************
from platform import node
import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog
import tkinter.simpledialog as simpledialog
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import threading
import keyboard
import random
import os
import pygetwindow as gw
import pyautogui
import time
import threading
from random import randint
import math
import ClusterHsm as clst

# import WsnRoutPwr as rout

# **************************************************************
# Set the initial line thickness and color
node = []  # WsnNodes[] Localize at regular interval=> [ndx][sno,x,y,pow,state]
tx_delay = []  # transmit delay in mSec
packet = []  # [pktno,srcno,dstno,fromno,hopno,type]; type=>0:adm,1:msg,2:ack
packetold = []  # [pktno,srcno,dstno,fromno,hopno,type]
mynodes = []  # [ndx][n1,n2,n3,..,nn]; all nearest nodes n1,n2 in range txrange
pair = []  # list of nearest node paires of commen nearest nodes
nodexy = []  # localized nodes=>[ndx][sno,x,y,state]
screen_width = 0
screen_height = 0
distmax = 0
txrange = 100
grpsize = 4
srcno = 0
dstno = 0
pkthopno = 0
fromno = 0
line_thickness = 1
line_color = "black"
nodemx = "100"
rout_speed = 0.1000
auto = False
loop = 0
drawing = False
go = True
nodeerr = []
gridX, gridY = 4, 3
ofsX, ofsY = 22, 110
test_acos = 0
test_sin = 0
test_cos = 0
area_min = 9999
sink = (-50, -50)
tx_range = 20  # 20% of distmax

# Function timer event ****************************************
def timer_event():
    global count, minerr, grpsize
    draw_grps()
    optimize_grps()
    if far_nod_err<minerr:
        minerr=far_nod_err
        
    # Code to execute when the timer event occurs
    print("Timer event occurred!")
    count = count + 1
    if(count<5):
        timer = threading.Timer(0.100, timer_event)
        timer.start()
    else:    
        count = 0
        if minerr>0:
            grpsize=grpsize+1
            text_grpmx.delete(0, tk.END)  # Clear existing text
            text_grpmx.insert(tk.END, str(grpsize))
            timer = threading.Timer(0.10, timer_event)
            timer.start()
            a=123
        print("Timer event completed.")
        
# Function to open the popup window ***************************
def open_popup_max_nodes():
    global nodemx
    nodemx = int(text_ndmx.get())
    default_text = str(nodemx)
    text = simpledialog.askstring(
        "Enter Text", "Enter Max Nodes:", initialvalue=default_text
    )
    if text:
        nodemx = int(text)
        text_ndmx.delete(0, tk.END)  # Clear existing text
        text_ndmx.insert(tk.END, str(nodemx))


# Function to open the popup window **************************
def open_popup_transmit_range():  # set transmit_range in % of max distance
    global tx_range, text_txrng
    default_text = str(tx_range * 100.0 / dstMx)
    text = simpledialog.askstring(
        "Enter Text", "Enter Max Nodes:", initialvalue=default_text
    )
    if text:
        dt = float(text)
        tx_range = int(dt * dstMx / 100.0)
        text_txrng.delete(0, tk.END)  # Clear existing text
        text_txrng.insert(tk.END, str(text))
        # set mynodes


# Function to open the popup window **************************
def open_popup_max_groups():
    global grpsize
    if grpsize > 7:
        grpsize = 7
    if grpsize < 2:
        grpsize = 2
    default_text = str(grpsize)
    text = simpledialog.askstring(
        "Enter Text", "Enter Average Hops:", initialvalue=default_text
    )
    if text:
        grpsize = int(text)
        text_grpmx.delete(0, tk.END)  # Clear existing text
        text_grpmx.insert(tk.END, str(grpsize))


# Function auto_grouping ************************************
def auto_grouping():
    global count,grpsize,minerr
    clst.nodes = node
    clst.populate_mynodes(txrange)
    grpsize=2
    text_grpmx.delete(0, tk.END)
    text_grpmx.insert(tk.END, str(grpsize))
    nodGrp = clst.make_nodGrp(nodemx, grpsize)  # number of nodes per cluster
    # mnd = clst.mynodes[3]  # ??????????????
    minerr=1000 # any big number
    timer = threading.Timer(0.10, timer_event)
    timer.start()
    count = 0

    a = 123


# Populate node[] with (sno,x,y,pow,grp **********************
def GetRandomNodes(nods, gapx, wdt, gapy, hgt):
    global node, txrange, nodexy, gridX, gridY
    global screen_width, screen_height, ofsX, ofsY
    grds = gridX * gridY
    ndPerGrd = nods / grds
    nn = 0
    nnOld = 0
    grpSz = []
    sum1 = 0
    tst = 0
    for y in range(gridY):
        for x in range(gridX):
            sum1 = sum1 + ndPerGrd
            nn = int(sum1 + 0.5)
            grpSz.append(nn - nnOld)
            nnOld = nn
            tst = tst + grpSz[len(grpSz) - 1]
    dx = (screen_width - ofsX) / gridX
    dy = (screen_height - ofsY) / gridY
    no = 0
    arr1 = []
    for y in range(gridY):
        yc = int(y * dy)
        for x in range(gridX):
            xc = int(x * dx)
            for n in range(grpSz[no]):
                col1 = []
                point = [
                    xc + random.randrange(0, int(dx - 10)),
                    yc + random.randrange(0, int(dy - 10)),
                ]
                col1.append(point[0])  # x
                col1.append(point[1])  # y
                col1.append(no)  # sno
                col1.append(100)  # pow
                col1.append(0)  # state
                arr1.append(col1)
            no = no + 1
    arr1.sort()
    node = []  # class WsnNodes[]
    nodexy = []
    for i in range(nods):
        node.append([i, arr1[i][0], arr1[i][1], arr1[i][3], arr1[i][4]])
        dt = [node[i][0], 0.0, 0.0, 0]  # [sno, x, y, flg]
        nodexy.append(dt)
    brk = 123


# Draw node[] with sno ****************************************
def draw_nodes():
    global nodemx, screen_width, screen_height, distmax, txrange, distmax, nodeerr
    global gridX, gridY, ofsX, ofsY, text_ndmx
    nodemx = int(text_ndmx.get())
    nodeerr = []
    mxnodes = int(nodemx)
    canvas.config(width=screen_width, height=screen_height)
    canvas.delete("all")
    nods = mxnodes
    GetRandomNodes(nods, 10, screen_width - ofsX, 10, screen_height - ofsY)
    draw_grid()
    for i in range(len(node)):
        draw_this_node(i, "blue", 2, "white")
        nodeerr.append(0)
    draw_sink(sink, "green", 4, "yellow")
    canvas.pack()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / grpsize
    a = 123


# Draw Grid ***************************************************
def draw_grid():
    global nodemx, screen_width, screen_height, gridX, gridY, ofsX, ofsY
    gapx = (screen_width - ofsX) / gridX
    gapy = (screen_height - ofsY) / gridY
    for x in range(gridX + 1):
        xl = x * gapx
        canvas.create_line(
            xl, 0, xl, screen_height - 1, width=1, fill="#CCCCCC"
        )  # draw line
    for y in range(gridY + 1):
        yl = y * gapy
        canvas.create_line(
            0, yl, screen_width - 1, yl, width=1, fill="#CCCCCC"
        )  # draw line


# Re-Draw Nodes ***********************************************
def re_draw_nodes():
    global nodemx, nodexy
    mxnodes = int(nodemx)
    canvas.delete("all")
    for i in range(len(node)):
        draw_this_node(i, "blue", 2, "white")
        nodexy[i][1] = 0  # [ndx][sno,x,y,state]
        nodexy[i][2] = 0  # [ndx][sno,x,y,state]
        nodexy[i][3] = 0  # [ndx][sno,x,y,state]
    draw_sink(sink, "green", 4, "yellow")
    canvas.pack()
    a = 123


# Draw One Node node[ndx] of width wdt ************************
def draw_this_node(ndx, col, wdt, bcol):
    global node
    r = True
    canvas.create_oval(
        node[ndx][1],
        node[ndx][2],
        node[ndx][1] + 20,
        node[ndx][2] + 20,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        node[ndx][1] + 10,
        node[ndx][2] + 10,
        text=str(node[ndx][0]),
        fill="red",
        font=("Helvetica 10 bold"),
    )
    return r


# Draw One Node nodexy[ndx] of width wdt **********************
def draw_sink(sink, col, wdt, bcol):
    global node
    r = True
    canvas.create_oval(
        sink[0],
        sink[1],
        sink[0] + 40,
        sink[1] + 40,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        sink[0] + 20,
        sink[1] + 20,
        text="SINK",
        fill="red",
        font=("Helvetica 10 bold"),
    )
    return r


# get distance between n1,n2 ***********************************
def distance_n1_n2(n1, n2):
    d1x = node[n1][1]
    d1y = node[n1][2]
    d2x = node[n2][1]
    d2y = node[n2][2]
    dst2 = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
    dst2 = round(dst2, 3)
    return dst2
    a = 123


# **************************************************************
def find_nearesr_node(x, y):
    global node
    dmn = distmax
    nmn = -1
    for i in range(len(node)):
        d = abs(node[i][1] - x) + abs(node[i][2] - y)
        if dmn > d:
            dmn = d
            nmn = node[i][0]

    return nmn


# *********************************************
def draw_grps():
    global lbl_scor, grpsize, tx_range
    tx_range = float(text_txrng.get()) * dstMx / 100.0
    grpsize = int(text_grpmx.get())
    grs = grpsize  # input number of clusters
    clst.nodes = node
    nodGrp = clst.make_nodGrp(nodemx, grs)  # number of nodes per cluster
    clst.GetClusterArray()  # main clustering algorithm
    lbl_scor.config(text="Len:100")
    draw_wsn()
    a = 123


# *********************************************
def draw_wsn():
    global far_nod_err
    canvas.delete("all")
    dist = 0
    far_nod_err = 0
    for val in range(len(clst.nodes)):
        n1 = clst.nodes[val][3]
        x1 = clst.nodes[val][1] + 10
        y1 = clst.nodes[val][2] + 10
        x2 = clst.nodes[n1][1] + 10
        y2 = clst.nodes[n1][2] + 10
        if distance_n1_n2(n1, val) >= tx_range:
            canvas.create_line(x1, y1, x2, y2, width=3, fill="red")
            far_nod_err = far_nod_err + 1
        else:
            canvas.create_line(x1, y1, x2, y2, width=3, fill="blue")  # draw line
        dist += math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
        err = ""
        if far_nod_err > 0:
            err = " Err:" + str(far_nod_err)
    lbl_scor.config(text="Len:" + str(int(dist)) + err)
    for val in range(len(clst.nodes)):
        canvas.create_oval(
            clst.nodes[val][1],
            clst.nodes[val][2],
            clst.nodes[val][1] + 20,
            clst.nodes[val][2] + 20,
            fill="white",
            outline="red",
        )  # draw nodes
        canvas.create_text(
            clst.nodes[val][1] + 10,
            clst.nodes[val][2] + 10,
            text=str(clst.nodes[val][0]),
            fill="red",
            font=("Helvetica 10 bold"),
        )  # draw nodes number
    draw_sink(sink, "green", 4, "yellow")
    canvas.pack()


# *********************************************
def optimize_grps():
    global dstMxoptimize_grpserr
    count = 0
    for i in range(len(clst.nodes)):
        d1x = clst.nodes[i][1]
        d1y = clst.nodes[i][2]
        ghi = clst.nodes[i][3]
        dstmn = dstMx
        jj = -1
        for j in range(len(clst.nodes)):
            ghj = clst.nodes[j][3]
            if ghj == j:
                d2x = clst.nodes[j][1]
                d2y = clst.nodes[j][2]
                dst = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
                if dstmn > dst:
                    dstmn = dst
                    jj = j
        if ghi != jj:
            clst.nodes[i][3] = jj
            count += 1
    draw_wsn()
    a = 123


# Remove Sink *************************************************
def remove_sink():
    global sink
    sink = (-50, -50)
    re_draw_nodes()
    a = 123


# Mouse event handlers *****************************************
def on_mouse_press3(event):
    global mouse_position
    x, y = event.x, event.y
    mouse_position = (x, y)


# Mouse event handlers ****************************************
def on_mouse_press(event):
    global drawing, nodexy, mouse_position, chkbx_sink, sink
    x, y = event.x, event.y
    mouse_position = (x - 20, y - 20)
    if chkbx_sink.get() == 1:
        chkbx_sink.set(0)
        sink = mouse_position
        re_draw_nodes()


# **************************************************************
def on_mouse_release(event):
    global drawing, go
    drawing = False
    go = False


# **************************************************************
def on_mouse_move(event):
    if drawing:
        global mouse_position
        x, y = event.x, event.y
        mouse_position = (x, y)


# **************************************************************
def get_area(n1, n2, n3):
    a = distance_n1_n2(n1, n2)
    b = distance_n1_n2(n1, n3)
    c = distance_n1_n2(n2, n3)
    s = (a + b + c) / 2.0
    ss = s * (s - a) * (s - b) * (s - c)
    area = 0
    if ss >= 0:
        area = math.sqrt(ss)
    return area


# **************************************************************
def open_file():
    global node, nodexy, txrange
    flnm = filedialog.askopenfilename(
        initialdir="", filetypes=(("data files", "*.txt"), ("all files", "*.*"))
    )
    file1 = open(flnm, "r")
    wrd = file1.readline().removesuffix("\n").split(",")
    flnm = wrd[0]
    sz = int(wrd[1])
    node = []
    nodexy = []
    for i in range(sz):
        wrd = file1.readline().removesuffix("\n").split(",")
        row = []
        row.append(int(wrd[0]))  # sno
        row.append(int(wrd[1]))  # x
        row.append(int(wrd[2]))  # y
        row.append(int(wrd[3]))  # pow
        row.append(int(wrd[4]))  # state
        node.append(row)
        dt = [int(wrd[0]), 0.0, 0.0, 0]  # [sno, x, y, flg]
        nodexy.append(dt)
    file1.close()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / grpsize
    re_draw_nodes()


# **************************************************************
def save_file():
    flnm = asksaveasfile(
        initialfile="LocalizeHsm.txt",
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
    )
    file2 = open(flnm.name, "w")
    sz = len(node)  # node: [ndx][sno,x,y,pow,state]
    pag = flnm.name + "," + str(sz) + "\n"
    for i in range(sz):
        line = node[i]
        pag += (
            str(line[0])  # sno
            + ","
            + str(line[1])  # x
            + ","
            + str(line[2])  # y
            + ","
            + str(line[3])  # pow
            + ","
            + str(line[4])  # state
            + "\n"
        )
    file2.writelines(pag)
    file2.close()


# **************************************************************
def save_image_file():
    flnm = asksaveasfile(
        initialfile="ClusterHsm.jpg",
        defaultextension=".jpg",
        filetypes=[("All Files", "*.*"), ("Image File", "*.jpg")],
    )
    # Find the application window by its title
    window_title = "WSN Clustering-HSM"
    app_window = gw.getWindowsWithTitle(window_title)[0]
    # Get the window's position and size
    left, top, width, height = (
        app_window.left,
        app_window.top,
        app_window.width,
        app_window.height,
    )
    # Capture the screenshot of the application window
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # Save the screenshot as a JPEG file
    screenshot.save(flnm)


# **************************************************************
def on_resize(event):
    # Get the new size of the form
    global canvas, screen_width, screen_height
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width, screen_height = width - 4, height - 41
    # canvas.config(width=screen_width, height=screen_height)
    a = 123


# **************************************************************
def main_menu():
    global window, canvas, screen_width, screen_height, text_txrng, distmax
    global gridX, gridY, dstMx, lbl_scor, text_ndmx, text_grpmx, chkbx_sink
    window.title("WSN Clustering-HSM")
    window.bind("<Configure>", on_resize)  # Configure the resize event handler

    # Create a Canvas widget
    # screen_width = window.winfo_screenwidth() / 1
    # screen_height = window.winfo_screenheight() / 1
    screen_width, screen_height = 800, 600
    # Create the status bar.....................................
    status_bar = tk.Frame(window, bd=1, relief=tk.SUNKEN)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    lbl_txrng = tk.Label(status_bar, text="Tx Rng %")  # Create a lablr
    lbl_txrng.pack(side=tk.LEFT, fill=tk.X)
    text_txrng = tk.Entry(status_bar, width=5)  # Create Tx Rng TextBox
    text_txrng.pack(side=tk.LEFT, fill=tk.X)
    text_txrng.insert(tk.END, "20")
    lbl_ndmx = tk.Label(status_bar, text=" Mx Nod")  # Create a lablr
    lbl_ndmx.pack(side=tk.LEFT, fill=tk.X)
    text_ndmx = tk.Entry(status_bar, width=5)  # Create Mx Nod TextBox
    text_ndmx.pack(side=tk.LEFT, fill=tk.X)
    text_ndmx.insert(tk.END, "100")
    lbl_grpmx = tk.Label(status_bar, text=" Mx Grp")  # Create a lablr
    lbl_grpmx.pack(side=tk.LEFT, fill=tk.X)
    text_grpmx = tk.Entry(status_bar, width=3)  # Create Mx Grp TextBox
    text_grpmx.pack(side=tk.LEFT, fill=tk.X)
    text_grpmx.insert(tk.END, "5")
    btn_nodes = tk.Button(
        status_bar, text="Nodes", command=lambda: draw_nodes()
    )  # Create Nodes button
    btn_nodes.pack(side=tk.LEFT)
    btn_clust = tk.Button(
        status_bar, text="Cluster", command=lambda: draw_grps()
    )  # Create Cluster button
    btn_clust.pack(side=tk.LEFT)
    btn_imprv = tk.Button(
        status_bar, text="Optimiz", command=lambda: optimize_grps()
    )  # Create Optimiz button
    btn_imprv.pack(side=tk.LEFT)
    btn_atogrp = tk.Button(
        status_bar, text="AtoGrp", command=lambda: auto_grouping()
    )  # Create Auto Grouping button
    btn_atogrp.pack(side=tk.LEFT)
    lbl_scor = tk.Label(  # Create a label
        status_bar, text="Score:    ", bd=1, anchor=tk.W
    )
    lbl_scor.pack(side=tk.RIGHT, fill=tk.X)
    # End Create status bar.....................................
    ofsX, ofsY = 0, 0
    dstMx = math.sqrt(
        screen_width * screen_width + screen_height * screen_height
    )  # default number of clusters
    canvas = tk.Canvas(window, width=screen_width, height=screen_height)
    canvas.pack()
    # window.state("zoomed") # Maximize the window
    menubar = tk.Menu(window)  # Create a menu bar
    window.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)  # Create the file menu
    menubar.add_cascade(label="File", menu=file_menu)
    tool_menu = tk.Menu(menubar, tearoff=0)  # Create the tool menu
    menubar.add_cascade(label="Tool", menu=tool_menu)

    # Add options to the file menu
    file_menu.add_command(label="Max Nodes ", command=lambda: open_popup_max_nodes())
    file_menu.add_command(label="Groups ", command=lambda: open_popup_max_groups())
    file_menu.add_command(
        label="Tx Range ", command=lambda: open_popup_transmit_range()
    )
    file_menu.add_command(label="AutoGroups ", command=lambda: auto_grouping())
    file_menu.add_command(label="Draw Nodes (cnt+d)", command=lambda: draw_nodes())
    file_menu.add_command(label="ReDraw Nodes (cnt+r)", command=lambda: re_draw_nodes())
    file_menu.add_command(label="Cluster Nodes (cnt+c)", command=lambda: draw_grps())
    file_menu.add_command(
        label="Optimize Nodes (cnt+o)", command=lambda: optimize_grps()
    )
    file_menu.add_separator()
    file_menu.add_command(label="Open Nodes", command=lambda: open_file())
    file_menu.add_command(label="Save Nodes", command=lambda: save_file())
    file_menu.add_command(label="Save Image (cnt+i)", command=lambda: save_image_file())
    file_menu.add_separator()
    file_menu.add_command(label="Exit (cnt+x)", command=window.quit)
    # Add options to the tool menu
    chkbx_sink = tk.IntVar()
    chkbx_sink.set(0)
    tool_menu.add_checkbutton(label="Place Sink", variable=chkbx_sink)
    tool_menu.add_command(label="Remove Sinc", command=lambda: remove_sink())
    # register the hotkey using the keyboard library
    keyboard.add_hotkey("ctrl+d", draw_nodes)
    keyboard.add_hotkey("ctrl+r", re_draw_nodes)
    keyboard.add_hotkey("ctrl+c", draw_grps)
    keyboard.add_hotkey("ctrl+o", optimize_grps)
    keyboard.add_hotkey("ctrl+i", save_image_file)
    keyboard.add_hotkey("ctrl+x", window.quit)
    # Bind the mouse event handlers to the canvas
    canvas.bind("<ButtonPress-3>", on_mouse_press3)
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)
    canvas.bind("<B1-Motion>", on_mouse_move)

    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    window.mainloop()  # Run the main loop


# Start the program ********************************************
window = tk.Tk()
print(os.path.dirname(__file__))
main_menu()

# **************************************************************
