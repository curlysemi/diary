import Tkinter, tkSimpleDialog
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox

import diary_io

root = Tkinter.Tk(className=" diary")

HEIGHT = 10

text_pads = []

def add_textpad():
    new_tp = ScrolledText(root, height=HEIGHT)
    new_tp.grid(row=len(text_pads))
    text_pads.append(new_tp)

def remove_textpad(forceDelete = False):
    # We'll always leave 1
    if text_pads and (forceDelete or len(text_pads) > 1):
        last_tp = text_pads[-1]
        last_tp.grid_forget()
        text_pads.remove(last_tp)

def get_password(prompt = 'Enter a password:'):
    return  tkSimpleDialog.askstring('Password', prompt, show='*')


# def open_command():
#     file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
#     if file != None:
#         contents = file.read()
#         textPad.insert('1.0',contents)
#         file.close()

def save_command():
    message_password_pairs = []
    for tp in text_pads:
        message = tp.get('1.0', END+'-1c')
        password = get_password('Enter a password (for "' + message[0:7].replace('\n','') + '"):')
        message_password_pairs.append((message, password))
    print(message_password_pairs)
    entry = diary_io.create_entry(message_password_pairs)
    diary_io.save_entry(entry)
    for i in range(len(text_pads)):
        remove_textpad(True)
    add_textpad()
        
def exit_command():
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def about_command():
    label = tkMessageBox.showinfo("About", "diary\nThis is a proof of concept.\ndeveloped by {;\nMIT License")
        

def dummy():
    print "I am a Dummy Command, I will be removed in the next step"
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=dummy)
menu.add_command(label="Add Msg", command=add_textpad)
menu.add_command(label="Remove Msg", command=remove_textpad)
# filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
# filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

add_textpad()
root.mainloop()