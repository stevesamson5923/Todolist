import libraries as lib
import todo_db as td
root = lib.tk.Tk()

root.geometry(f"{lib.WIDTH}x{lib.HEIGHT}+0+0")
root.resizable(0,0)
root.title("Timetable Management System")
root.configure(background='white')       
root.bind("<Escape>", lambda e: e.widget.destroy())            
#m = itf.MainWindow(root,'Class Timetable','3 timetable found')

top_frame_color='#eb3b28'
bottom_frame_color = '#c70670'
frame_color= '#f07d71'
date_color= '#d4cbcf' 


top_frame = lib.Frame(root,width=lib.WIDTH,height=100,bg=top_frame_color)
top_frame.pack(side='top',expand=1,fill='both')
bottom_frame = lib.Frame(root,width=lib.WIDTH,height=590,bg=bottom_frame_color)
bottom_frame.pack_propagate(0)
bottom_frame.pack()

todo_list = []
td.connect_to_mysql()
current_todo_no = 0

class ScrollableFrame(lib.ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = lib.tk.Canvas(self,bg='#fff')
        scrollbar = lib.ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = lib.ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


scroll_f = ScrollableFrame(bottom_frame)
scroll_f.pack(expand=True,fill='both')


#frame_list=[]
#for i in range(50):
#f1 = lib.Frame(f.scrollable_frame).pack(side='top')
#f1 = lib.Frame(f.scrollable_frame,width=200,height=30)
#b = lib.Button(f1,text='First Button')
#b1 = lib.Button(f1,text='Second Button')
#b.pack(side='left',padx=20)
#b1.pack(side='left')
#f1.pack()
#frame_list.insert(i,f1)

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
    id = lib.random.randint(100,200)
    if response:
        for r in response:
            if r[0] == id:
                id = get_id()
                return id
            else:
                return id
        return id
    else:
        return id

def add_todo(event):
    global ffff,loading
    f1 = lib.Frame(scroll_f.scrollable_frame,width=1000,height=60,bg='#fff')
    f1.pack_propagate(0)

    id = 100
    id = get_id()   
    #print('fff', id)
    #print('Yes',event.widget.get()) 
    title = event.widget.get()
    dt = lib.datetime.today()
    todo = Todo(f1,id,title,dt,0) #bottom_frame
    td.insert_todo(id,title,dt.strftime('%y-%m-%d'),0)
    set_current_todo_no(get_current_todo_no()+1)
    with open('todono.txt','w') as f:
        f.write(str(get_current_todo_no()))
    f1.pack(expand=True,fill='both',padx=180,pady=10)
    
    #todo.pack_propagate(0)
    #todo.pack(side='top',padx=20,pady=10)
    #todo_list.insert(get_current_todo_no(),f1)
    
    #td.close()


todo_entry = lib.Entry(top_frame,font=('Lucida Sans',11),width=100)
todo_entry.focus()
todo_entry.pack(padx=20,pady=20,ipadx=15,ipady=5)
todo_entry.bind('<Return>',add_todo)

class Todo():
    def __init__(self,frame1,id,title,dt,prog):
        #super(Todo, self).__init__(master=bottom_frame,width=300,height=60)
        #Frame.__init__(self, master)
        self.progress = prog #0 means unfinished 1 means finished
        self.tid = id
        self.left_frame = lib.tk.Frame(frame1,width=1360,bg=frame_color)
        self.left_frame.bind('<Button-1>',self.call)
        self.left_frame.pack_propagate(0)
        self.title = lib.tk.Label(self.left_frame,text = title,fg='white',bg=frame_color,font=('Lucida Sans',12,'bold'),wraplength=250)
        self.edit_icon = lib.ImageTk.PhotoImage(lib.Image.open('edit.png').resize((24,24)))
        self.edit = lib.tk.Label(self.left_frame,image=self.edit_icon,bg=frame_color)
        self.edit.bind('<Button-1>',self.edit_title)
        self.entry_box = lib.Entry(self.left_frame,font=('Lucida Sans',11),width=10)
        self.entry_box.bind('<Return>',self.change_title)
        self.entry_box.bind('<Escape>',self.keep_title)
        #self.CheckVar1 = lib.tk.IntVar()
        #self.C1 = lib.Checkbutton(self.left_frame, text = title,variable = self.CheckVar1, \
        #         onvalue = 1, offvalue = 0,fg='white',bg=frame_color,font=('Lucida Sans',12,'bold'),\
        #         wraplength=180,command=self.call)    
        self.dt= dt.strftime('%d-%m-%y')
        self.created_on = lib.tk.Label(self.left_frame,text='Created On : '+self.dt,bg=frame_color,fg='white',font=('Lucida Sans',8,'italic'))
        
        self.check_uncheck = lib.tk.Label(self.left_frame,bg=frame_color)
        #self.right_frame = tk.Frame(self,width=50,height=60,bg='white')
        #self.right_frame.pack_propagate(0)
        #self.arrow = ImageTk.PhotoImage(Image.open('left-arrow.png').resize((30,30)))
        #self.arrow_but = tk.Button(self.right_frame,image=self.arrow,bg='white',relief=tk.FLAT)
        if self.progress == 1:
            #MARKING AS COMPLETE
            self.left_frame.configure(bg='#56ed42')
            self.title.configure(bg='#56ed42')
            self.created_on.configure(bg='#56ed42')
            self.check_uncheck.configure(bg='#56ed42') 
            self.edit.configure(bg='#56ed42')
            check_image = lib.ImageTk.PhotoImage(lib.Image.open('check.png').resize((24,24)))
            self.check_uncheck.configure(image=check_image)
            self.check_uncheck.image = check_image                         
        else:
            self.left_frame.configure(bg=frame_color)
            self.title.configure(bg=frame_color)
            self.edit.configure(bg=frame_color)
            self.created_on.configure(bg=frame_color)
            self.check_uncheck.configure(bg=frame_color)  
            self.check_uncheck.configure(image='')
            self.check_uncheck.image = ''

        self.display()
    def keep_title(self,event):
        print('inside keep')
        self.title.grid(row=0,column=0,padx=5,pady=(5,1),sticky='w')
        self.entry_box.grid_forget()
    def change_title(self,event):
        new_title = event.widget.get()
        self.title.configure(text=new_title)
        self.title.grid(row=0,column=0,padx=5,pady=(5,1),sticky='w')
        self.entry_box.grid_forget()        
        td.update_title(self.tid,new_title)
    def edit_title(self,event):
        self.title.grid_forget()
        self.entry_box.grid(row=0,column=0,padx=5,pady=(5,1),sticky='w')
        self.entry_box.focus()
    def call(self,event):
        #print('Yes')
        #self.C1.toggle()
        if self.progress == 0:
            #MARKING AS COMPLETE
            self.left_frame.configure(bg='#56ed42')
            self.title.configure(bg='#56ed42')
            self.created_on.configure(bg='#56ed42')
            self.check_uncheck.configure(bg='#56ed42') 
            self.edit.configure(bg='#56ed42')
            check_image = lib.ImageTk.PhotoImage(lib.Image.open('check.png').resize((24,24)))
            self.check_uncheck.configure(image=check_image)
            self.check_uncheck.image = check_image                         
            self.progress = 1
            td.update_progress(self.progress,self.tid)
        else:
            self.left_frame.configure(bg=frame_color)
            self.title.configure(bg=frame_color)
            self.created_on.configure(bg=frame_color)
            self.check_uncheck.configure(bg=frame_color)  
            self.check_uncheck.configure(image='')
            self.check_uncheck.image = ''
            self.edit.configure(bg=frame_color)
            self.progress = 0
            td.update_progress(self.progress,self.tid)
    def display(self):
        self.left_frame.pack(side='left',expand=1,fill='both')
        self.title.grid(row=0,column=0,padx=5,pady=(5,1),sticky='w')
        self.edit.grid(row=0,column=1,padx=5,pady=(5,1))
        self.created_on.grid(row=1,column=0,padx=5,pady=(1,3),sticky='w')
        self.check_uncheck.grid(row=0,column=2,rowspan=2,padx=20,sticky='e')
        #self.right_frame.pack(side='left')
        #self.arrow_but.pack(side='left',padx=10)

def load_todo():
    result = td.show_all_todos()
    if result:        
        for r in result:
            f1 = lib.Frame(scroll_f.scrollable_frame,width=1000,height=60,bg='#fff')
            f1.pack_propagate(0)
            todo = Todo(f1,r[0],r[1],r[2],r[3]) #bottom_frame
            f1.pack(expand=True,fill='both',padx=180,pady=10)
    else:
        return
    
load_todo()

#for i in range(50):
#    frame_list[i].pack(padx=20,pady=10)
    



root.mainloop()