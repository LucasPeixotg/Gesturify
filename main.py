import threading
from components.gestureFrame import GestureFrame
from components.roundedButton import RoundedButton
from gestureRecognizer import GestureRecognizer

import tkinter as tk
from tkinter import ttk

from pallete import *
import time

import os

GESTURES = ['Closed_Fist', 'Victory', 'Open_Palm']
PROCESS_DELAY = 0.005

def process_gesture(recon, app):
    loading_value = 0
    current_gesture = 'None'
        
    while True:
        gesture = recon.current_gesture
        
        if gesture != current_gesture:
            if current_gesture in GESTURES: 
                app.load_gesture(current_gesture, 0)
            
            current_gesture = gesture
            loading_value = 0

        if gesture in GESTURES:

            loading_value += 1
            app.load_gesture(gesture, loading_value)            
            time.sleep(PROCESS_DELAY)
            
            if loading_value >= 360:
                os.system('./gestures/'+gesture+'/script.sh')
                app.destroy()

class App(tk.Tk):
    def __init__(self, gesture_options):
        super().__init__()

        #self.geometry('720x480')
        self.resizable(1, 1)

        ##
        # STYLE CONFIGURATION
        ##
        self.style = ttk.Style(self)
        
        #title bar styles
        self.style.configure('Titlebar.TFrame', font=('Helvetica', 11), background=BACKGROUND_COLOR, relief="flat")
        self.style.configure('Close.TButton', font=('Helvetica', 11))
        
        self.style.configure('Main.TFrame', background=BACKGROUND_COLOR, relief='flat')

        self.style.configure('Gesture.TFrame', background=BACKGROUND_COLOR2)


        ##
        # TITLE BAR 
        ##
        self.overrideredirect(True) # turns off title bar

        # make a frame for the title bar
        title_bar = ttk.Frame(self, style='Titlebar.TFrame', padding=10)

        # put a close button on the title bar        
        close_button = RoundedButton(parent=title_bar, font_size=10, width=20, height=20, bg=BACKGROUND_COLOR ,border_radius=10, color="#f02424", command=self.destroy)
 

       # pack the widgets
        title_bar.pack(expand=1, fill=tk.X)
        close_button.pack(side=tk.RIGHT)

        # bind title bar motion to the move window function
        title_bar.bind('<B1-Motion>', self.__move_window)
        
        ##
        
        ##
        # MAIN
        ##
        main = ttk.Frame(self, style="Main.TFrame", padding=20)

        ##
        
        ##
        # GESTURES
        ##
        self.gestures = {}
        for gesture in gesture_options:
            gesture_frame = GestureFrame(main, gesture=gesture, icon_path='gestures/'+gesture+'/icon.png')
            gesture_frame.pack(side=tk.RIGHT)
            
            self.gestures[gesture] = gesture_frame
            

        main.pack(expand=1, fill=tk.BOTH)
        
    def load_gesture(self, gesture, load_value):
        self.gestures[gesture].set_loading(load_value)

    def __move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


if __name__=="__main__":
    
    app = App(gesture_options=GESTURES)
    
    recognizer = GestureRecognizer()
    recognizer_thread = threading.Thread(target=recognizer.start, daemon=True)
    print_thread = threading.Thread(target=lambda: process_gesture(recognizer, app), daemon=True)
    
    recognizer_thread.start()
    print_thread.start()

    app.mainloop()
    