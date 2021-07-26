from tkinter import *
from tkinter import messagebox

import psycopg2
from setup import *

mn = Tk()


mn.geometry('500x450+500+200')
mn.title('PythonToDoList')
mn.config(bg='#223441')
mn.resizable(width=False, height=False)


frame = Frame(mn)
frame.pack(pady=10)

# connection db-------------------------------

connection = psycopg2.connect(
    user=USER, password=PASSWORD, host=HOST, port=PORT, database='todolist')
cursor = connection.cursor()

# create table in db
# create_table = """CREATE TABLE tasks(id INT PRIMARY KEY NOT NULL,
#                                     task_name VARCHAR(50) NOT NULL)"""
# cursor.execute(create_table)
# connection.commit()


# def ------


def newTask():
    task = my_entry.get()
    if task != "":
        select_task_db = """SELECT id from tasks"""
        cursor.execute(select_task_db)
        connection.commit()
        try:
            last_id = sorted(cursor.fetchall()[-1], reverse=True)
            new_id = last_id[0]
        except IndexError:
            new_id = 0
        

        insert_task_db = f"""INSERT INTO tasks VALUES({new_id+1},'{task}')"""
        cursor.execute(insert_task_db)
        connection.commit()
        lb.insert(END, task)
        my_entry.delete(0, "end")
    else:
        messagebox.showwarning("warning", "Please enter some task.")


def deleteTask():
    task_delete = my_entry.get()
    if task_delete != "":
        index_task = int(task_delete)
        delete_task = task_list[index_task-1]
        task_list.remove(delete_task)
        str_delete_task = ''.join(delete_task)
        print(str_delete_task)
       
    lb.delete(ANCHOR)

    delete_query = f"""DELETE FROM tasks WHERE task_name = '{str_delete_task}'"""
    cursor.execute(delete_query)
    connection.commit()


# # -----------------
lb = Listbox(
    frame,
    width=25,
    height=8,
    font=('Times', 18),
    bd=0,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none",

)
lb.pack(side=LEFT, fill=BOTH)


task_list = """SELECT task_name from tasks"""
cursor.execute(task_list)
connection.commit
task_list = cursor.fetchall()

for item in task_list:
    lb.insert(END, item)
sb = Scrollbar(frame)
sb.pack(side=RIGHT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)

my_entry = Entry(
    mn,
    font=('times', 24)
)
button_frame = Frame(mn)
button_frame.pack(pady=20)

my_entry.pack(pady=20)


addTask_btn = Button(
    button_frame,
    text='Add Task',
    font=('times 14'),
    bg='#c5f776',
    padx=20,
    pady=10,
    command=newTask
)
addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

delTask_btn = Button(
    button_frame,
    text='Delete Task',
    font=('times 14'),
    bg='#ff8b61',
    padx=20,
    pady=10,
    command=deleteTask
)
delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

mn.mainloop()

