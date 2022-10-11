#!/usr/bin/python
# select_directory.py
__author__  = "Griff Wood and Beckwith"
__version__ = "2.0"

"""Provides function to get directory"""

from tkinter import filedialog
from tkinter import *
import tkinter as tk

def get_directory():
    ''' Asks user to choose a location
    
    :return: Selected File Path as String
    '''
    root = tk.Tk()
    root.geometry('{}x{}'.format(0, 0)) #shrink extra tk window
    root.update()
    root.attributes("-topmost", True)  # bring window to front, so dialog will be up front

    # bring up ask directory dialog:
    dirname = filedialog.askdirectory(parent=root, initialdir="/")
    
    root.destroy()  
    
    return dirname

# TEST:
#print("Use the Open dialog to select directory to save to...")
#print("The directory you selected is:\n", get_directory())