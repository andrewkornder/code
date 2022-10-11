#!/usr/bin/env
#imageOpen.py
__author__ = "Beckwith, Fletcher, & online sources"
__version__ = "2.0"

'''
Provides a function to bring up a file open dialog box.  Much of the code is 
there to deal with tkinter issues that arise when trying to use askopenfilename.
2/2/18: confirmed functioning properly in all cases
'''

import tkinter as tk
from tkinter import filedialog as fd

def prompt_and_get_file_name(path):
    """prompt the user to open a file and return the file path of the file"""

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.geometry('{}x{}'.format(0, 0))
    root.update()
    
    # Get file name as string from user:
    img_file_name = fd.askopenfilename(
        initialdir=path,
        title="Select file",
        filetypes=
        (
            ("jpeg files", "*.jpg"),
            ("jpeg files", "*.jpeg"),
            ("png files", "*.png"),
            ("gif files", "*.gif")
        ),
        parent=root  
    )
    
    root.update()
    root.destroy()

    # return name of selected file as string; img_file_name with be "" if user hits cancel:
    if isinstance(img_file_name, str):
        return img_file_name
    # img_file_name would be tuple if user selects file then hits cancel, so must return "" instead
    else:
        return ""
