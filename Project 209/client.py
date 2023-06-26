import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
import os
import ntpath #This is used to extract filename from path
from ftplib import FTP
from tkinter import filedialog
from pathlib import Path

from playsound import playsound
import pygame
from pygame import mixer


def openChatWindow():

    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10))
    namelabel.place(x=10, y=8)

    infoLabel = Label(window, text= "", font = ("Calibri",10))
    infoLabel.place(x=10, y=28)

    name = Entry(window,width =30,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10), command=play)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10), command=stop)
    disconnectButton.place(x=350,y=160)

    pauseButton=Button(window,text="pasue",bd=1, font = ("Calibri",10), command=pause)
    pauseButton.place(x=350,y=160)

    resumeButton=Button(window,text="resume",bd=1, font = ("Calibri",10), command=resume)
    resumeButton.place(x=350,y=160)

    window.mainloop()

def play():
    global song_selected
    global infoLabel

    song_selected=listbox.get(ANCHOR)
    pygame
    mixer.init()
    mixer.music.load('shared_files'+song_selected)
    mixer.music.play()
    if(song_selected !=""):
        infoLabel.configure(text="Now playing " + song_selected)
    else:
        infoLabel.configure(text="")
    
def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text="")
    
def resume():
    global song_selected
    mixer.init()
    mixer.music.load('shared_files'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files'+song_selected)
    mixer.music.pause()

def browseFiles():
    global sending_file
    global textarea
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        filePathLabel.configure(text=filename)
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname=ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()
        
        message=("send "+fname)
        if(message[:4] == "send"):
            print("Please wait .....\n")
            textarea.insert(END,"\n"+"\nPlease wait .....\n")
            textarea.see("end")
            sending_file = message[5:]
            file_size = getFileSize("shared_files/"+sending_file)
            final_message = message + " " + str(file_size)
            SERVER.send(final_message.encode())
            textarea.insert(END,"In Process..")

       

    except FileNotFoundError:
        print("Cancle Button Pressed")


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    openChatWindow()

setup()