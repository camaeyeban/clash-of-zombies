#!/usr/bin/env python3
# Reference: ecs-network.serv.pacific.edu
# Set script as executable via: chmod +x chat.py
# Run via:  ./chat.py host port
# sudo apt-get install python3-tk

import socket
import select
import os
import sys
import tkinter
import _thread
import time
from ChatFns import *
from tkinter.scrolledtext import ScrolledText

def main():
    print("Starting Chatroom")

    # Instantiate class for UI
    ui = clientUI()

    # Run the UI, and capture CTRL-C to terminate
    try:
        ui.start()
    except KeyboardInterrupt:
        print("Caught CTRL-C, shutting down client")
        ui.eventDeleteDisplay()
    
    print("Closing Chatroom")


class clientUI():
    def __init__(self):
        self.first_click = True;

    def start(self):
        print("Starting clientUI...")
        self.initDisplay()

        if(len(sys.argv) < 3) :
            print('Usage : python chat.py hostname port name')
            sys.exit()
     
        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.name = str(sys.argv[3])

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(2)
        try:
            self.s.connect((self.host, self.port))
            LoadConnectionInfo(self.ui_messages, '[ Succesfully connected ]\n--------------------------------------------')
        except:
            LoadConnectionInfo(self.ui_messages, '[ Unable to connect ]')
            return

        self.ui_messages.insert(tkinter.END, "Welcome to Clash of Zombies! \n")

        def ReceiveData():
            
            while 1:
                socket_list = [sys.stdin, self.s]
                 
                # Get the list sockets which are readable
                read_sockets,write, error = select.select(socket_list , [], [])
                 
                for sock in read_sockets:
                    data = sock.recv(4096)
                    if not data :
                        LoadConnectionInfo(self.ui_messages, '[ Disconnected from chat server ]')
                        sys.exit()
                    else :
                        #print data
                        LoadConnectionInfo(self.ui_messages, data.decode("utf-8"))

        _thread.start_new_thread(ReceiveData,())
        # This call to mainloop() is blocking and will last for the lifetime
        # of the GUI.
        self.ui_top.mainloop()

        # Should only get here after destroy() is called on ui_top
        print("Stopping clientUI...")

    def initDisplay(self):
        self.ui_top = tkinter.Tk()
        self.ui_top.wm_title("Chatroom")
        self.ui_top.resizable('1','1')
        self.ui_top.protocol("WM_DELETE_WINDOW", self.eventDeleteDisplay)
        
        self.ui_messages = ScrolledText(
            master=self.ui_top,
            wrap=tkinter.WORD,
            width=50,  # In chars
            height=25)  # In chars     

        self.ui_input = tkinter.Text(
            master=self.ui_top,
            wrap=tkinter.WORD,
            width=50,
            height=4)
        
        # Bind the button-1 click of the Entry to the handler
        self.ui_input.bind('<Button-1>', self.eventInputClick)
        
        self.ui_button_send = tkinter.Button(
            master=self.ui_top,
            text="Send",
            command=self.sendMsg)


        # Compute display position for all objects
        self.ui_messages.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.ui_input.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.ui_button_send.pack(side=tkinter.LEFT)

    # SEND button pressed
    def sendMsg(self):
        # Get user input (minus newline character at end)
        msg = self.ui_input.get("0.0", tkinter.END+"-1c")

        if(msg != ""):
        	print("UI: Got text: '%s'" % msg)
        	LoadConnectionInfo(self.ui_messages, "<You> "+msg)
        
        # Clean out input field for new data
        self.ui_input.delete("0.0", tkinter.END)

        self.s.send(bytes(self.name + "\02" + msg, 'UTF-8'))

    # Event handler - User closed program via window manager or CTRL-C
    def eventDeleteDisplay(self):
        print("UI: Closing")

        # Continuing closing window now
        self.ui_top.destroy()

    # Event handler - User clicked inside the "ui_input" field
    def eventInputClick(self, event):
        if(self.first_click):
            # If this is the first time the user clicked,
            # clear out the tutorial message currently in the box.
            # Otherwise, ignore it.
            self.ui_input.delete("0.0", tkinter.END)
            self.first_click = False;


if __name__ == "__main__":
    sys.exit(main())
