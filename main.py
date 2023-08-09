import threading
from components.roundedButton import RoundedButton
from gestureRecognizer import GestureRecognizer

import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

from pallete import *

def process_gesture(recon):
    while True:
        #print(recon.current_gesture)
        pass


class App(tk.Tk):
    def __init__(self, gesture_options=['THUMBS UP', 'POINTING UP', 'sas']):
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
        for gesture in gesture_options:
            gesture_frame = tk.Frame(main, width=300, height=300, 
                highlightbackground=BACKGROUND_COLOR, highlightthickness=50)
            
            icon_render = ImageTk.PhotoImage(Image.open("open_palm.png"))
            img = tk.Label(gesture_frame, image=icon_render, bg=BACKGROUND_COLOR2)
            img.image = icon_render
            img.pack(side=tk.RIGHT)
            
            gesture_frame.pack(side=tk.RIGHT)
            

        main.pack(expand=1, fill=tk.BOTH)

    def __move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


if __name__=="__main__":
    recognizer = GestureRecognizer()
    recognizer_thread = threading.Thread(target=recognizer.start, daemon=True)
    print_thread = threading.Thread(target=lambda: process_gesture(recognizer), daemon=True)
    
    recognizer_thread.start()
    print_thread.start()

    app = App()
    app.mainloop()
    