#!/usr/bin/env python3
# Reference: cs-network.serv.pacific.edu
# Set script as executable via: chmod +x chat.py
# Run via:  ./chat.py
# sudo apt-get install python3-tk

import os
import sys
import tkinter
import time
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename

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

        self.ui_messages.insert(tkinter.END, "Adding a message to the text field...\n")
        self.ui_input.insert(tkinter.END, "<Enter message>")

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

        self.ui_button_file = tkinter.Button(
            master=self.ui_top,
            text="File",
            command=self.sendFile)

        # Compute display position for all objects
        self.ui_messages.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.ui_input.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.ui_button_send.pack(side=tkinter.LEFT)
        self.ui_button_file.pack(side=tkinter.RIGHT)


    # SEND button pressed
    def sendMsg(self):
        # Get user input (minus newline character at end)
        msg = self.ui_input.get("0.0", tkinter.END+"-1c")

        print("UI: Got text: '%s'" % msg)

        # Add this data to the message window
        self.ui_messages.insert(tkinter.INSERT, "%s\n" % (msg))
        self.ui_messages.yview(tkinter.END)  # Auto-scrolling
        
        # Clean out input field for new data
        self.ui_input.delete("0.0", tkinter.END)


    # FILE button pressed
    def sendFile(self):
        file = askopenfilename()

        if(len(file) > 0 and os.path.isfile(file)):
            print("UI: Selected file: %s" % file)
        else:
            print("UI: File operation canceled")

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
