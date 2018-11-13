import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox

root = Tkinter.Tk(className=" diary")

HEIGHT = 10

text_pads = []

def add_textpad():
    new_tp = ScrolledText(root, height=HEIGHT)
    new_tp.grid(row=len(text_pads))
    text_pads.append(new_tp)

def remove_textpad():
    # We'll always leave 1
    if text_pads and len(text_pads) > 1:
        last_tp = text_pads[-1]
        last_tp.grid_forget()
        text_pads.remove(last_tp)

# def open_command():
#     file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
#     if file != None:
#         contents = file.read()
#         textPad.insert('1.0',contents)
#         file.close()

# def save_command(self):
#     file = tkFileDialog.asksaveasfile(mode='w')
#     if file != None:
#         data = self.textPad.get('1.0', END+'-1c')
#         file.write(data)
#         file.close()
        
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
# filemenu.add_command(label="Save", command=save_command)
# filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

add_textpad()
root.mainloop()