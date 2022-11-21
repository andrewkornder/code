#!/usr/bin/python
# gui.py
'''UI for image processing project'''
__version__ = "1.0"
__author__ = 'beckwith'

import img_processing as ip  # you will write your functions in this module
import image_open  # for code to open image file with file dialog
import tkinter
from tkinter.font import Font
from PIL import Image

original_img = ""
new_image = ""

### fill in each of the 3 below for each new function ###
OPTIONS = [
    "Select Process:",  # [0]
    "Inversion",  # [1]
    "Darken",  # [2]
    "Greyscale",  # [3]
    "Black and White",  # [4]
    "Filter",  # [5]
    "Edge Detection",  # [6]
    "Shrink",  # [7]
    "Spot the Difference",  # [8]
    "Picture Frame",  # [9]
    "Pixelate",  # [10]
    "highest pixel",
    'add noise'
]

# dictionary for instructions:
INSTRUCTIONS = {
    OPTIONS[0]: "",
    OPTIONS[1]: "This will invert the colors of your image.  \nSelect an image and " + \
                "hit the START button to begin",
    OPTIONS[2]: "Select an image, give an amount in the first box, then hit the START button",
    OPTIONS[3]: "Select an image then hit START",
    OPTIONS[4]: "Select an image then hit START",
    OPTIONS[5]: "Put the limits on the red, green and blue value in the boxes.",
    OPTIONS[6]: "Select an image then hit START",
    OPTIONS[7]: "Add a resolution that has the same ratio of your image in the format 900x600",
    OPTIONS[8]: "Add two images that have some pixels different between them. The images should be the same size",
    OPTIONS[9]: "Add an image and then a size for the border in the first box",
    OPTIONS[10]: 'Select an image and then put a size for each \'pixel\' in the first box ',
    OPTIONS[11]: 'Select an image then hit START',
    OPTIONS[12]: 'Add an amount of noise to add in the first box, select an image then hit START'
}
# dictionary for functions
FUNCTIONS = {
    OPTIONS[0]: None,
    OPTIONS[1]: ip.inversion,
    OPTIONS[2]: ip.lighten_darken,
    OPTIONS[3]: ip.grayscale,
    OPTIONS[4]: ip.black_white,
    OPTIONS[5]: ip.rgbfilter,
    OPTIONS[6]: ip.edge_detection,
    OPTIONS[7]: ip.shrink,
    OPTIONS[8]: ip.spot_diff,
    OPTIONS[9]: ip.border,
    OPTIONS[10]: ip.pixelate,
    OPTIONS[11]: ip.highest_pixel,
    OPTIONS[12]: ip.noise
}

root = tkinter.Tk()  # the base window that all tkinter objects go into
root.title("\u2192\u2192\u2192 IMAGE PROCESSING \u27FF\u27FF\u27FF")
root.geometry("1000x400")
root.configure(background='grey')


###################################
# FUNCTIONS CALLED BY MENU AND BUTTONS:
###################################

def quitting_time():
    '''called when Quit button is pressed'''
    root.quit()


def large_display(instructions):
    '''
    sets text in large display
    
    :param instructions: instructions to display
    '''
    instructions_display.configure(state="normal")  # allow editing of text
    instructions_display.delete(1.0, tkinter.END)  # delete previous text
    instructions_display.insert(tkinter.END, instructions)  # show results in text area
    instructions_display.configure(state="disabled")  # prevent editing of text


def show_instructions(event):
    '''Called when menu item is selected and will show instructions'''

    selection = menu_var.get()  # get which item was selected
    instructions = INSTRUCTIONS[selection]
    #### PUT YOUR INSTRUCTIONS HERE #### 
    large_display(instructions)


def process():
    '''called when the process button is clicked'''

    global menu_var, instructions_display, entry_1, entry_2, entry_3
    global entry_4, input_area, results_label

    global original_img, new_image
    # gets values (as strings) from the entry boxes
    arg_1 = entry_1.get()
    arg_2 = entry_2.get()
    arg_3 = entry_3.get()

    # get selected function and process image!!!!
    fn = None
    selection = menu_var.get()
    fn = FUNCTIONS[selection]
    # original_img = Image.open(original_img)
    if fn is not None and original_img is not None:
        results_label.config(text="Working...")
        ##### call process function, sending it any agruments it needs #####

        '''if selection in (OPTIONS[1], OPTIONS[3], OPTIONS[4], OPTIONS[6]):  # use or for any other functions that
                                     # have only the image as an argument
            new_image = fn(original_img)'''
        # EXAMPLE OF THOSE NEEDING MORE ARGUMENTS:
        if selection in [OPTIONS[2], OPTIONS[7], OPTIONS[9], OPTIONS[10], OPTIONS[12]]:
            new_image = fn(original_img, arg_1)
        elif selection in [OPTIONS[5]]:
            new_image = fn(original_img, arg_1, arg_2, arg_3)
        elif selection == OPTIONS[8]:
            img2 = original_img
            select_img()
            new_image = fn(original_img, img2)
        else:
            new_image = fn(original_img)

        results_label.config(text="Done!")
        # deletes old text and insert results text into the large text area:
        large_display("")

    elif fn is None:
        msg = "No process selected or not ready yet"
        if original_img is None:
            msg += "\nNo image selected!"
        results_label.config(text=msg)


def select_img():
    '''calls code to bring up file open dialog and get image path'''
    global original_img
    image_folder = "./images/"

    original_img_path = image_open.prompt_and_get_file_name(image_folder)

    # show file path in label in gui:
    if original_img_path == "":
        file_msg = "NO IMAGE FILE SELECTED!"
    else:
        file_msg = "FILE:" + original_img_path
        original_img = Image.open(original_img_path)

    results_label.config(text=file_msg)


def show():
    global new_image
    if new_image != "":
        ip.show(new_image)
    else:
        results_label.config(text="Select and process image first!")


def save():
    global new_image
    if new_image != "":
        ip.save(new_image)
    else:
        results_label.config(text="Select and process image first!")


def main():
    global menu_var, instructions_display, entry_1, entry_2, entry_3
    global entry_4, input_area, results_label
    ###################################
    # SET UP ALL THE DISPLAY COMPONENTS:
    ###################################

    # nice font:
    my_font = Font(family="Verdana", size=15, weight="bold")
    my_font2 = Font(family="Verdana", size=11, weight="bold")

    ###################################
    # 1. TEXT AREA THAT DISPLAYS RESULTS, USING THE ABOVE FONT
    ###################################
    instructions_display = tkinter.Text(root,  # display needs the tkinter window to be put in
                                        height=10,
                                        relief="ridge",
                                        bd=6,
                                        width=60,
                                        font=my_font,
                                        foreground='white',
                                        background='black')

    photo = tkinter.PhotoImage(file='python_icon.gif')  # fun photo to display at start
    # (PhotoImages must be .gif)

    instructions_display.configure(state="normal")  # allow editing of text
    instructions_display.image_create(tkinter.END, image=photo)  # inserts fun photo
    instructions_display.insert(tkinter.END, "Welcome to Image Processing using Python!")  # insesrts default text
    instructions_display.configure(state="disabled")

    ###################################
    # 3. TEXT LABEL THAT CAN SHOW RESULTS:
    ###################################
    results_label = tkinter.Label(text="STATUS INFO", foreground="red",
                                  background="black")  # default text is 'other values'

    ###################################
    # 4. BUTTONS
    ###################################

    # will call the select() function when pressed:
    select_img_button = tkinter.Button(text="SELECT IMG", command=select_img,
                                       foreground="green")
    select_img_button.config(font=my_font)
    # will call the process() function when pressed:
    process_button = tkinter.Button(text="===> START", command=process,
                                    foreground="blue")
    process_button.config(font=my_font2)

    show_button = tkinter.Button(text="SHOW", command=show, foreground="purple")
    show_button.config(font=my_font2)

    save_button = tkinter.Button(text="SAVE", command=save, foreground="red")
    save_button.config(font=my_font2)

    # will call quitting_time when pressed:
    quit_button = tkinter.Button(root, text="Quit", command=quitting_time,
                                 foreground="red")
    quit_button.config(font=my_font2)

    ###################################
    # 5. SET UP PULLDOWN MENU OF FUNCTION CHOICES:
    ###################################

    # this variable holds the selected value from the menu
    menu_var = tkinter.StringVar(root)
    menu_var.set(OPTIONS[0])  # default value

    # create the optionmenu (pulldown menu) with the options above:
    option_menu = tkinter.OptionMenu(root, menu_var, *OPTIONS,
                                     command=show_instructions)
    option_menu.config(font=my_font, foreground="brown")

    ###################################
    # 6. PLACE EVERYTHING IN THE TKINTER WINDOW:
    #     a "grid" allows you to turn the tkinter window into a series
    #     of rows and columns and specifcy where to place everything
    ###################################

    select_img_button.grid(row=0, column=0, columnspan=1, padx=10, pady=10,
                           ipadx=5, ipady=5)

    # place the menu in the top left:
    option_menu.grid(row=0, column=1, columnspan=1, padx=10, pady=10,
                     ipadx=5, ipady=5)

    # place the buttons in the top middle:
    process_button.grid(row=0, column=2, columnspan=1, padx=10, pady=10,
                        ipadx=5, ipady=5)
    show_button.grid(row=0, column=3, columnspan=1, padx=10, pady=10,
                     ipadx=5, ipady=5)
    save_button.grid(row=0, column=4, columnspan=1, padx=10, pady=10,
                     ipadx=5, ipady=5)
    quit_button.grid(row=5, column=2, columnspan=3, padx=10, pady=10,
                     ipadx=5, ipady=5)

    # sets up argument input boxes...ADD MORE IF YOU NEED THEM!!!
    entry_1 = tkinter.Entry()  # makes an Entry object
    entry_2 = tkinter.Entry()
    entry_3 = tkinter.Entry()

    # place the entry boxes in the next row, going across...ADD MORE IF NEEDED!!!
    entry_1.grid(row=1, column=0)
    entry_2.grid(row=1, column=1)
    entry_3.grid(row=1, column=2)

    # place the label in the next row (is just one row of text):
    results_label.grid(row=3, column=0, columnspan=5)

    # place the text areas in the next row (is a whole box of text):
    instructions_display.grid(row=4, column=0, columnspan=6)
    # make it so that words won't get broken up when reach end of text box:
    instructions_display.config(wrap=tkinter.WORD)

    # waits for button clicks to take actions:
    root.mainloop()


if __name__ == "__main__":
    main()
