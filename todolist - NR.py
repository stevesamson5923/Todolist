import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
from tkinter import messagebox, Scrollbar,Canvas
from tkinter import Menu, filedialog
from PIL import ImageTk, Image
import random
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
import random
import threading
import time
import webbrowser
import urllib.request
import requests
import json
import cloudinary.uploader
from cloudinary import CloudinaryImage 
import os
import todo_db as td
import mainframe as mf

root = tk.Tk()

WIDTH=270
HEIGHT=400

top_frame_color='#a1035a'
bottom_frame_color = '#c70670'
frame_color= '#7d0546'
date_color= '#d4cbcf' 

root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(0,0)
root.title("Todo List")
root.focus_set()
root.configure(background='white')
#root["bg"] = "black"
root.bind("<Escape>", lambda e: e.widget.destroy())

top_frame = Frame(root,width=WIDTH,height=80,bg=top_frame_color)
top_frame.pack(side='top',expand=1,fill='both')
bottom_frame = Frame(root,width=WIDTH,height=320,bg=bottom_frame_color)
bottom_frame.pack_propagate(0)
bottom_frame.pack()

ffff = mf.ScrollableFrame(bottom_frame)
ffff.pack()

todo_list = []
td.connect_to_mysql()
current_todo_no = 0

def get_current_todo_no():
    return current_todo_no

def set_current_todo_no(no):
    global current_todo_no
    current_todo_no = int(no)

try:
    with open('todono.txt','r') as f:
        no = f.read()
        if no:
            set_current_todo_no(int(no))
        else:
            set_current_todo_no(0)
except:
    set_current_todo_no(0)
            

def get_id():
    response = td.show_all_todos()
    id = random.randint(100,200)
    for r in response:
        if r[0] == id:
            id = get_id()
            return id
        else:
            return id
    return id
def add_todo(event):
    global ffff
    id = 100
    id = get_id()   
    print('fff', id)
    #print('Yes',event.widget.get())
    title = event.widget.get()
    dt = datetime.today()
    todo = Todo(id,ffff.scrollable_frame,title,dt) #bottom_frame
    todo.pack_propagate(0)
    todo.pack(side='top',padx=20,pady=10)
    todo_list.insert(get_current_todo_no(),todo)
    set_current_todo_no(get_current_todo_no()+1)
    td.insert_todo(id,title,dt.strftime('%y-%m-%d'),0)
    with open('todono.txt','w') as f:
        f.write(str(get_current_todo_no()))
    #td.close()

todo_entry = Entry(top_frame,font=('Lucida Sans',11))
todo_entry.focus()
todo_entry.pack(padx=20,pady=20,ipadx=15,ipady=5)
todo_entry.bind('<Return>',add_todo)

class Todo(tk.Frame):
    def __init__(self,id,bottom_frame,title,dt):
        super(Todo, self).__init__(master=bottom_frame,width=300,height=60)
        #Frame.__init__(self, master)
        self.tid = id
        self.left_frame = tk.Frame(self,width=250,height=60,bg=frame_color)
        self.left_frame.pack_propagate(0)
        self.title = tk.Label(self.left_frame,text=title,fg='white',bg=frame_color,font=('Lucida Sans',10),wraplength=180)
        self.dt= dt.strftime('%d-%m-%y')
        self.created_on = tk.Label(self.left_frame,text='Last modified : '+self.dt,bg=frame_color,fg=date_color,font=('Lucida Sans',8,'italic'))
        self.right_frame = tk.Frame(self,width=50,height=60,bg='white')
        self.right_frame.pack_propagate(0)
        self.arrow = ImageTk.PhotoImage(Image.open('left-arrow.png').resize((30,30)))
        self.arrow_but = tk.Button(self.right_frame,image=self.arrow,bg='white',relief=tk.FLAT)
        self.display()
    def display(self):
        self.left_frame.pack(side='left',expand=1,fill='both')
        self.title.grid(row=0,column=0,padx=5,pady=(5,1),sticky='w')
        self.created_on.grid(row=1,column=0,padx=5,pady=(1,3),sticky='w')
        self.right_frame.pack(side='left')
        self.arrow_but.pack(side='left',padx=10)

root.mainloop()