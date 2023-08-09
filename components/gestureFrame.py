import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from pallete import *

class GestureFrame(tk.Canvas):
    def __init__(self, root, gesture, icon_path):
        super().__init__(root, width=300, height=300, 
            highlightbackground=BACKGROUND_COLOR, highlightthickness=50, bg=BACKGROUND_COLOR)
        
        icon_render = ImageTk.PhotoImage(Image.open(icon_path))
        self.icon_render = icon_render
        self.create_image((200, 200), image=icon_render)
        
        self.loading_id = self.create_arc(50, 50, 150, 150,
            start=0, extent=0, fill=SECONDARY_COLOR,
            width=0, style='pieslice', outline='')

    
    def set_loading(self, quantity=0):
        '''
        Changes display according to the quantity loaded
        Quantity must be a number between 0 and 1
        '''
        if quantity >= 360:
            quantity = 360

        self.itemconfigure(self.loading_id, {'extent': quantity})
        