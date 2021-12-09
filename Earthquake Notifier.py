import re
import os
import json
import time
from tkinter import*
import urllib.request
from time import sleep
from win10toast import ToastNotifier
from tkinter import Tk, Frame, Canvas, ALL, NW

giventheok = 0

url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'

window = Tk()
window.title('Earthquake Dekstop Notifier')
c = Canvas(window, height=400, width=500, bg='black')
c.pack()

def startupchecks():
    global delaytime, d1, d2
    f = open("directory1.txt", "r")
    ds = f.read()
    f.close()

    d1 = ds + 'quakelog.txt'
    d2 = ds + 'quakebackup.txt'
    
    try:
        f = open(d1, "r")
        f.close()
    except:
        f = open(d1, "w")
        f.close()
    try:
        f = open(d2, "r")
        f.close()
    except:
        f = open(d2, "w")
        f.close()
    delaytime = 30
    print('startup checks done')


def getquakes():
    global whatisit, ifany
    print('getting earthquake list')
    thing = json.load(urllib.request.urlopen(url))
    listOfQuakes = []
    numQuakes = len(thing['features'])
    for i in range(0,numQuakes):
        title = thing['features'][i]['properties']['title']
        details = title.split(",")
        state = details[-1]
        if ('California' in state) or ('CA' in state) or ('OR' in state) or ('Oregon' in state) or ('Washington' in state) or ('WA' in state) or ('Hawaii' in state) or ('HI' in state) or ('Alaska' in state) or ('AK' in state):
            epochTime = thing['features'][i]['properties']['updated']
            listOfQuakes.append(str(epochTime) + " - " + title)
    listOfQuakes.sort()
    
    file = open(d1, 'r')
    tocopy = file.read()
    file.close()
    file = open(d2, 'r')
    tobackup = file.read()
    file.close()
    file = open(d2, 'w')
    file.write(tobackup)
    file.write('\n')
    file.write(tocopy)
    file.close()
    
    for quake in listOfQuakes:
        components = quake.split("-")
        epochTime = components[0]
        quakeDate = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.localtime(float(epochTime)/1000))
        title = components[2]
        magnitude = components[1]
        magnitude = re.sub('[M]', 'Magnitude:', magnitude)
        f = open(d1, "r")
        before = f.read()
        f.close()
        try:
            print(quakeDate + " | " + title + " | " + magnitude)
        except:
            print("Couldn't Print Quake")
        try:
            f = open(d1, "w")
            f.write(before)
            f.write("\n")
            f.write(str(quakeDate + " | " + title + " | " + magnitude))
            f.close()
        except Exception as e:
            print("Couldn't Write Quake to File " + d1)
            print(e)
    print("comparing for new earthquakes")
    with open(d1, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        numero1 = f.readline().decode()

    with open(d2, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        numero2 = f.readline().decode()
    
    print("last earthquakes from lists:")
    print('Current List: ' + numero1)
    print('Before List: ' + numero2)
    if numero1 != numero2:
        print("\n")
        print("\n")
        print("new earthquakes detected:")
        try:
            print(numero1)
        except:
            print("1Notification Can\'t Be Delivered")
        try:
            n = ToastNotifier()
            thingy = numero1
            n.show_toast("New Earthquake Found", str(thingy), duration = 30,
            icon_path ="Untitled.ico")
            whatisit = str(thingy)
            ifany = 1
        except:
            print("2Notification Can't Be Delivered")
        
    else:
        print("\n")
        print("\n")
        print("no new earthquakes detected")
        ifany = 0
        whatisit = ''


startupchecks()

nocare = 0

lecommand = False

def go1():
    window.destroy()
    giventheok = 1
    print('running in background')
    lecommand = True
    while lecommand:
        getquakes()
        sleep(delaytime)
def go2():
    global ifany, whatisit
    giventheok = 1
    print('running in foreground')
    lecommand = True
    while lecommand:
        c.delete("all")
        label = c.create_text(100,30,
                              text='Getting Earthquakes...', fill='white', font=('Times New Roman', 15))
        label2 = c.create_text(195,60,
                              text='Program May Stop Responding Several Times,', fill='white', font=('Times New Roman', 15))
        label3 = c.create_text(110,90,
                              text='While Updating the Lists', fill='white', font=('Times New Roman', 15))

        window.update()
        getquakes()
        window.update()
        c.delete("all")
        window.update()
        ###
        if ifany == 1:
            label = c.create_text(100,30,
                              text='Earthquake Found:', fill='white', font=('Times New Roman', 15))
            label2 = c.create_text(100,60,
                              text=whatisit, fill='white', font=('Times New Roman', 15))
            window.update()
        if ifany == 0:
            window.update()
            label = c.create_text(100,30,
                              text='No New Earthquake(s) Found:', fill='white', font=('Times New Roman', 15))
        ###
        sleep(delaytime)
def go3():
    lecommand = False
    print('Enter New Interval Between Updates (In Seconds)')
    lething = input('')
    file = open('delaytime.txt', 'w')
    file.write(lething)
    file.close()
    print('Interval Updated')

def go4():
    lecommand = False
    print('Enter A New FULL Directory To Save Logs To')
    lething = input('')
    if ((lething == '') or (lething == ' ')):
        lething == ds
        print('Since a blank was issued, no changes will be made')
    file = open('directory1.txt', 'w')
    file.write(lething)
    file.close()
    print('Directory Updated')

button1 = Button(window, text = "Run In Background", command = go1, anchor = W)
button1.configure(width = 20, activebackground = "#FFFFFF", relief = FLAT)
button1_window = c.create_window(10, 300, anchor=NW, window=button1)

button2 = Button(window, text = "Run In Foreground", command = go2, anchor = W)
button2.configure(width = 20, activebackground = "#FFFFFF", relief = FLAT)
button2_window = c.create_window(150, 300, anchor=NW, window=button2)

button3 = Button(window, text = "Change Update Freq", command = go3, anchor = W)
button3.configure(width = 20, activebackground = "#FFFFFF", relief = FLAT)
button3_window = c.create_window(300, 300, anchor=NW, window=button3)

button4 = Button(window, text = "Change Directories", command = go4, anchor = W)
button4.configure(width = 20, activebackground = "#FFFFFF", relief = FLAT)
button4_window = c.create_window(10, 325, anchor=NW, window=button4)

while True:
    try:
        window.update()
    except:
        nocare += 1
        if nocare >= 3:
            nocare = 0
    sleep(0.1)




