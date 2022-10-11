from tkinter import filedialog
def get_file(directory='./'):
    """prompt the user to open a file and return it"""
    text_file_name = ""
    #open dialog for file/open:
    # TO DO: add other file types!!!!!!!!!!!!!!!!!!
    try:
        text_file_name = filedialog.askopenfilename(
            initialdir=directory,
            title="Select file",
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            ))


    except:
        print("Text file not able to be opened")
    return text_file_name