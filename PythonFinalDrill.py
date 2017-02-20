"""
File Mover
Jamie W Bryant
"""
#Imports
import shutil, sys, time, os
import tkinter as tk
from tkinter import *
import tkinter.filedialog
import sqlite3
from datetime import datetime, timedelta

#Open and or connect to Sqlite3 database
conn = sqlite3.connect('pythontime.db', isolation_level=None)
c = conn.cursor()

#Create table if not
def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS updateTime(lastUpdated TEXT)')

#Insert time of file move
def insertTime():
    c.execute("INSERT INTO updateTime VALUES(datetime())")

#Execute createTable
createTable()

#User selects source
def askSource():
  sorName = filedialog.askdirectory()
  if sorName:
    varS.set(sorName)

#User selects destination
def askDestination():
  desName = filedialog.askdirectory()
  if desName:
    varD.set(desName)

#Source print or user type
def sorInput(status,name):
  sorFrame = Frame(root, bg="green")
  sorLabel = Label(sorFrame, fg="green")
  sorLabel["text"] = name
  sorLabel.grid(row=0,column=0)
  text = status
  varS = StringVar(root)
  varS.set(text)
  s = Entry(sorFrame, textvariable= varS).grid(row=0,column=1)
  
  sorFrame.grid(row=0)
  return s, varS

#Destination print or user type
def desInput(statusD,nameD):
  desFrame = Frame(root, bg="red")
  desLabel = Label(desFrame, fg="red")
  desLabel["text"] = nameD
  desLabel.grid(row=1,column=0)
  text = statusD
  varD = StringVar(root)
  varD.set(text)
  d = Entry(desFrame, textvariable= varD).grid(row=1,column=1)
  
  desFrame.grid(row=4)
  return d, varD

#def Print_entry():
#  print (varS.get(), varD.get())

#Moves files and resets update time
def fileMove():
        source = varS.get()
        dest = varD.get()
        files = os.listdir(source)
        max_id.set(datetime.now())
        now = time.time()
        insertTime()
        
        for f in files:
            src = source + "/" + f
            dst = dest + "/" + f
            if os.stat(src).st_mtime > now - 1 * 86400:
                if os.path.isfile(src):
                    shutil.move(src, dst)
                    print("File move is Alright, Alright, Alright")


#Root with GUI 
root = Tk()
root.title("File Mover")
root.maxsize(width=250, height=150)
root.minsize(width=250, height=150)
root.resizable(width=NO, height=NO)

#Pulls last update time from table
c.execute('SELECT max(lastUpdated) FROM updateTime')
max_id=StringVar()
max_id.set(c.fetchone()[0])

#Label displays last update
label3=Label(root, textvariable=max_id, fg='Red').grid(row=5,column=0)

#Move button
getBut = Button(root, text='Move', bg = "blue", fg="black", command = fileMove).grid(row=10,column=0)

#Destination button
dirBut = Button(root, text='Arrive', bg = "red", fg="green", command = askDestination).grid(row=4,column=3)

#Source button
dirBut = Button(root, text='Source', bg = "green", fg="red",command = askSource).grid(row=0,column=3)





s, varS = sorInput("", "Source")
d, varD = desInput("", "Arrive")
root.mainloop()
