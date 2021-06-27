import mysql.connector as sql

db_cursor = None
db_connection = None

def connect_to_mysql():
    global db_cursor,db_connection
    db_connection = sql.connect(host='localhost', database='class11', user='root', password='Steve751989')
    db_cursor = db_connection.cursor()
    db_cursor.execute("create table if not exists Todo(todo_id varchar(10) primary key,title varchar(50),dt date)")

def close():
    db_cursor.close()
    db_connection.close()
    
def insert_todo(tid,title,todo_dt,progress):
    global db_cursor,db_connection
    query = "insert into Todo values(%s,%s,%s,%s)"
    db_cursor.execute(query,(tid,title,todo_dt,progress))
    db_connection.commit()
    #print(db_cursor.rowcount, " record inserted.")

def update_title(tid,new_title):
    global db_cursor,db_connection
    query = "update Todo set title=%s where todo_id=%s"
    db_cursor.execute(query,(new_title,tid))
    db_connection.commit()

def find_todo_by_id_name(id):
    global db_cursor,db_connection
    query = "select * from todo where id=%s"
    db_cursor.execute(query,(id,))
    result = db_cursor.fetchall()
    return result
    
def show_all_todos():
    global db_cursor,db_connection
    query = "select * from Todo"
    db_cursor.execute(query)
    result = db_cursor.fetchall()  
    #print(result)
    return result

def update_progress(prog,id):
    global db_cursor,db_connection
    query = "update Todo set progress=%s where todo_id=%s"
    db_cursor.execute(query,(prog,id))
    db_connection.commit()
    print('Updated')
    
def delete_all():
    query = "delete from Todo"
    db_cursor.execute(query)
    db_connection.commit()
    print('DELETED')

def delete_book_by_id(bid):
    print('deleting...')
    query = 'delete from Todo where todo_id='+str(bid)
    db_cursor.execute(query)
    db_connection.commit()
    return 1

connect_to_mysql()
#delete_all()
#show_all_todos()
#a = delete_book_by_id(102)
#print(a)
close()
#insert_todo(102,'World tour','2020-11-20')