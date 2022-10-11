import tkinter

def widgets():
    
    tkinter.Label(root, text='Your Name:').grid(row=0, column=3, columnspan=2, pady=3)
    tkinter.Entry(root).grid(row=1, column=3, columnspan=2)
    
    t = tkinter.Text(root)
    t.grid(row=3, column=0, columnspan=3)
    
    t.insert(1.0, 'Give your reason for choosing this language')
    
    tkinter.Checkbutton(root, text='Java').grid(row=2, column=0)
    tkinter.Checkbutton(root, text='Python').grid(row=2, column=1)
    tkinter.Checkbutton(root, text='C++').grid(row=2, column=2)
    tkinter.Button(root, text='Okay').grid(row=2, column=3, pady=3, padx=20)
    tkinter.Button(root, text='Cancel').grid(row=2, column=4, pady=3, padx=20)
    
def create_window():
    global root 
    root = tkinter.Tk()
    root.title('Programming Language')
    root.configure(bg='powderblue')
    root.geometry('800x600')
    
    widgets()
    root.mainloop()

if __name__ == '__main__':
    create_window()