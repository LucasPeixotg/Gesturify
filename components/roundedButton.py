from tkinter import *
import tkinter as tk
import tkinter.font as font

class RoundedButton(tk.Canvas):
  def __init__(self, parent, border_radius, width=20, height=20, padding=0, bg='#000000' ,color='#ffffff', text='', command=None, font_size=10):
    tk.Canvas.__init__(self, parent, borderwidth=0,
                       relief="raised", highlightthickness=0, bg=bg)
    self.command = command
    
    self.font = font.Font(size=font_size, family='Helvetica')
    self.id = None
    height = height
    width = width
    
    if border_radius > 0.5*width:
      print("Error: border_radius is greater than width.")
      border_radius=0

    if border_radius > 0.5*height:
      border_radius=0
      print("Error: border_radius is greater than height.")

    rad = 2*border_radius

    def shape():
      self.create_arc((0, rad, rad, 0),
                      start=90, extent=90, fill=color, outline=color)
      self.create_arc((width-rad, 0, width,
                        rad), start=0, extent=90, fill=color, outline=color)
      self.create_arc((width, height-rad, width-rad,
                        height), start=270, extent=90, fill=color, outline=color)
      self.create_arc((0, height-rad, rad, height), start=180, extent=90, fill=color, outline=color)
      return self.create_polygon((0, height-border_radius, 0, border_radius, border_radius, 0, width-border_radius, 0, width,
                           border_radius, width, height-border_radius, width-border_radius, height, border_radius, height),
                                 fill=color, outline=color)

    id = shape()
    (x0, y0, x1, y1) = self.bbox("all")
    width = (x1-x0)
    height = (y1-y0)
    self.configure(width=width, height=height)
    self.create_text(width/2, height/2,text=text, fill='black', font= self.font)
    self.bind("<ButtonPress-1>", self._on_press)
    self.bind("<ButtonRelease-1>", self._on_release)

  def _on_press(self, event):
      self.configure(relief="sunken")

  def _on_release(self, event):
      self.configure(relief="raised")
      if self.command is not None:
          self.command()