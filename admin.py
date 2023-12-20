import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
from tkinter import messagebox
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import text
import psycopg2
import sqlite3 as sq

root=ttk.Window(themename="morph")
root.title('Панель администратора')
# root.iconbitmap('')
root.geometry("1300x800")
root.resizable(False,False)
root.config(bg="grey")

# con=sq.connect('db.db')
# cursor=con.cursor()
engine =create_engine('postgresql+psycopg2://postgres:12345@127.0.0.1:5432/postgres')
con=engine.connect()
# query='select * from practice.state'
# results = con.execute(query).fetchall()

# проверка подключения  
# with engine.connect() as connection:
#     result = connection.execute("SELECT 1")
#     print(result.fetchone())

# --- атрибуты для добавления проекта
lab_add = ttk.Label(root, text='Добавить проект',font=("Courier New",10,"bold"))
label_add = ttk.Label(root, text='Добавить проект',font=("Courier New",15,"bold"))
lab_name=ttk.Label(root, text='Название',font=("Courier New",10,"bold"))
lab_desc=ttk.Label(root, text='Описание',font=("Courier New",10,"bold"))
lab_state=ttk.Label(root, text='Статус',font=("Courier New",10,"bold"))
lab_start=ttk.Label(root, text='Дата начала',font=("Courier New",10,"bold"))
lab_end=ttk.Label(root, text='Дата завершения',font=("Courier New",10,"bold"))
lab_user=ttk.Label(root, text='Участники и роли',font=("Courier New",10,"bold"))
lab_manager=ttk.Label(root, text='ФИО менеджера по проекту',font=("Courier New",8,"bold"))
lab_skill=ttk.Label(root, text='Навыки',font=("Courier New",10,"bold"))

states=['Готов','В процессе','Просрочен']
comb_state=ttk.Combobox(root,values=states)
comb_state.current(1)

global ent_users
ent_users=ttk.Entry(root)
ent_name=ttk.Entry(root)
ent_desc=ttk.Entry(root)
ent_start=ttk.Entry(root)
ent_end=ttk.Entry(root)
ent_manager=ttk.Entry(root)
global ent_role
ent_role=ttk.Entry(root)
ent_skills=ttk.Entry(root,width=30)
# - для ввода роли и имени

entries = {"ent{}".format(i): ttk.Entry(root) for i in range(1, 11)}
y_position = 200
y_pos=200
entries2 = {"ent2{}".format(i): ttk.Entry(root) for i in range(1, 11)}

# -
# ---атрибуты для изменения проекта
lable_edit = ttk.Label(root, text='Редактор проектов',font=("Courier New",15,"bold"))
lable_edit.place(x=10,y=10)
lab_choose=ttk.Label(root, text='Поиск проекта',font=("Courier New",10,"bold"))
lab_edit=ttk.Label(root, text='Какой столбец?',font=("Courier New",10,"bold"))
lab_str=ttk.Label(root, text='Условие',font=("Courier New",10,"bold"))

entry_name=ttk.Entry(root)
entry_name.insert(0, "Введите название")
entry_desc=ttk.Entry(root)
entry_desc.insert(0, "Или описание")
ent_values=ttk.Entry(root)
ent_values.insert(0, "На что меняем?")
ent_find=ttk.Entry(root)
ent_find.insert(0, "Введите то, что выбрали")

types=['Статус','Название','Описание','Дата начала','Дата завершения','Навыки','Видимость']
comb_edit=ttk.Combobox(root,values=types)
comb_edit.current(0)
value=['По id','По ключевому слову']
comb_find=ttk.Combobox(root,values=value)
comb_find.current(0)

query='select id,name,description,day_start,day_end,skills,state from practice.project'
results = con.execute(query).fetchall()
columns = ['№', 'Статус', 'Название', 'Описание', 'Дата начала','Дата завершения','Навыки','Видимость']
tree = ttk.Treeview(root, columns=columns, show='headings',height=15)
tree.column('№', width=40)
tree.column('Название', width=100)
tree.column('Описание', width=130)
tree.column('Статус', width=100)
tree.column('Дата начала', width=150)
tree.column('Дата завершения', width=150)
tree.column('Навыки',width=130)
tree.column('Видимость', width=90)
for i in columns:
            tree.heading(i, text=i)
for i in results:
    tree.insert('', index=ttk.END, values=i)
# --- атрибуты для изменения участников проекта
label_change= ttk.Label(root, text='Редактор участников',font=("Courier New",15,"bold"))
lab_find=ttk.Label(root, text='Найти участника',font=("Courier New",10,"bold"))
lab_editman=ttk.Label(root, text='Какой столбец?',font=("Courier New",10,"bold"))
lab_strman=ttk.Label(root, text='Условие',font=("Courier New",10,"bold"))

ent_findman=ttk.Entry(root)
ent_valuesman=ttk.Entry(root)
ent_valuesman.insert(0, "На что меняем?")
ent_insert=ttk.Entry(root)
ent_insert.insert(0, "Введите то, что выбрали")

typesss=['Имя','Номер команды']
comb_editman=ttk.Combobox(root,values=typesss)
comb_editman.current(0)

que='select * from practice.student'
res = con.execute(que).fetchall()
columns = ['№', 'Фамилия', 'Имя', 'Отчество']
tree_stud = ttk.Treeview(root, columns=columns, show='headings',height=15)
for i in columns:
            tree_stud.heading(i, text=i)
for i in res:
    tree_stud.insert('', index=ttk.END, values=i)
# ---функция добавления проекта
def add_proj():
    clear()
    label_add.place(x=400,y=10)
    lab_name.place(x=350,y=60)
    ent_name.place(x=350,y=100)
    lab_desc.place(x=350,y=150)
    ent_desc.place(x=350,y=190)
    lab_state.place(x=350,y=240)
    comb_state.place(x=350,y=280)
    lab_start.place(x=350,y=330)
    ent_start.place(x=350,y=370)
    ent_start.insert(0, "2020-11-11")
    lab_end.place(x=350,y=420)
    ent_end.place(x=350,y=460)
    ent_end.insert(0, "2023-10-01")
    lab_user.place(x=700,y=60)
    lab_manager.place(x=700,y=100)
    ent_manager.place(x=1050,y=90)
    lab_skill.place(x=350,y=510)
    ent_skills.place(x=350,y=550)
    ent_skills.insert(0,'Перечислите через запятую')
    btn_save.place(x=350,y=610)
    btn_plus.place(x=800,y=150)
    btn_min.place(x=870,y=150)
    y_position = 200
    y_pos=200
    for entry in entries.values():
        entry.place(x=700, y=y_position)
        y_position += 50
    for entry2 in entries2.values():
        entry2.place(x=930, y=y_pos)
        y_pos+= 50
        

# тут реализована функция, с помощью которой можно удобно собрать команду 

def add_name():
    global y_position
    if y_position < 10:
        ent = ttk.Entry(root)
        ent.place(x=700, y=y_position)
        entries["ent{}".format(len(entries)+1)] = ent
        y_position += 50
def drop_name():
    global entries, y_position
    if entries:
        ent = entries.pop("ent{}".format(len(entries)))
        ent.place_forget()
        y_position -= 50

def drop():
     drop_name()
     drop_role()

def add_role():
    global y_pos, entries2
    if y_pos < 10:
        ent2 = ttk.Entry(root)
        ent2.place(x=930, y=y_position)
        entries2["ent2{}".format(len(entries2)+1)] = ent2
        y_pos += 50
def drop_role():
    global entries2, y_pos
    if entries:
        ent2 = entries2.pop("ent2{}".format(len(entries2)))
        ent2.place_forget()
        y_pos -= 50

def add():
     add_role()
     add_name()

def save_update_proj():
    namep=ent_name.get()
    desc=ent_desc.get()
    state=comb_state.get()
    day_start=ent_start.get()
    day_end=ent_end.get()
    skills=ent_skills.get()
    manager_input = ent_manager.get()
    parts = manager_input.split()
    surname = parts[0]
    name = parts[1]
    patronymic = parts[2]
    
    query=text(f"INSERT INTO practice.project(name,description,day_start,day_end,skills,state) values (:namep,:desc,:day_start,:day_end,:skills,:state) RETURNING id")
    project_id = con.execute(query, namep=namep, desc=desc, day_start=day_start, day_end=day_end, skills=skills, state=state).fetchone()[0]

    q_manager=text(f"INSERT INTO practice.student(f_name,s_name,l_name) values (:name,:surname,:patronymic) RETURNING id")
    student_id = con.execute(q_manager, name=name, surname=surname, patronymic=patronymic).fetchone()[0]
    
    que=text(f"INSERT INTO practice.groupp(student_id, project_id, role) values (:stud_id, :project_id, :role_input)")
    con.execute(que, stud_id=student_id, project_id=project_id, role_input='Проектный менеджер')

    for entry in entries.values():
        user_input = entry.get()
        parts = user_input.split()
        surname = parts[0]
        name = parts[1]
        patronymic = parts[2]
        for entry2 in entries2.values():
            role_input=entry2.get()
            q=text(f"INSERT INTO practice.student(f_name,s_name,l_name) values (:name,:surname,:patronymic) RETURNING id")
            stud_id=con.execute(q, name=name, surname=surname, patronymic=patronymic).fetchone()[0]
            con.execute(que, stud_id=stud_id, project_id=project_id, role_input=role_input)
            que=text(f"INSERT INTO practice.groupp(student_id, project_id, role) values (:stud_id, :project_id, :role_input)")
            con.execute(que, stud_id=student_id, project_id=project_id, role_input=role_input)
    

#-- функция для очицения
def clear():
    label_add.place_forget()
    lab_name.place_forget()
    ent_name.place_forget()
    lab_desc.place_forget()
    ent_desc.place_forget()
    lab_state.place_forget()
    comb_state.place_forget()
    btn_save.place_forget()
    lable_edit.place_forget()
    lab_user.place_forget()
    tree.place_forget()
    lab_choose.place_forget()
    entry_desc.place_forget()
    entry_name.place_forget()
    btn_find.place_forget()
    comb_edit.place_forget()
    lab_edit.place_forget()
    ent_values.place_forget()
    lab_str.place_forget()
    comb_find.place_forget()
    ent_find.place_forget()
    btn_snupd.place_forget()
    lab_manager.place_forget()
    ent_manager.place_forget()
    ent_role.place_forget()
    lab_start.place_forget()
    lab_end.place_forget()
    ent_start.place_forget()
    ent_end.place_forget()
    label_change.place_forget()
    ent_findman.place_forget()
    comb_editman.place_forget()
    ent_valuesman.place_forget()
    btn_findman.place_forget()
    btn_editman.place_forget()
    lab_editman.place_forget()
    lab_find.place_forget()
    ent_insert.place_forget()
    lab_strman.place_forget()
    lab_skill.place_forget()
    ent_skills.place_forget()
    btn_min.place_forget()
    btn_plus.place_forget()
    tree_stud.place_forget()
    for entry in entries.values():
        entry.place_forget()
    for entry2 in entries.values():
        entry2.place_forget()

# функция для реадктирования проекта
def edit_proj():
    clear()
    lable_edit.place(x=600,y=10)
    lab_choose.place(x=80,y=300)
    entry_name.place(x=80,y=350)
    entry_desc.place(x=80,y=400)
    btn_find.place(x=80,y=450)
    lab_edit.place(x=80,y=530)
    comb_edit.place(x=80,y=570)
    ent_values.place(x=80,y=630)
    lab_str.place(x=400,y=530)
    comb_find.place(x=400,y=570)
    ent_find.place(x=400,y=630)
    btn_snupd.place(x=80,y=700)
    tree.place(x=380,y=60)
# функция, которая сохраняет изменения в бд и обновляет таблицу в приложении
def save_and_update():
     global tree
     column=comb_edit.get()
     value=ent_values.get()
     id_or_key=comb_find.get()
     req=ent_find.get()
     if column=='Название':
        column='name'
     elif column=='Описание':
          column='description'
     elif column=='Статус':
        column='state'
     else:
          column='group_id'
          
     
     if id_or_key == 'По id':
        query="UPDATE practice.proects SET {columns} = ? WHERE id = ?".format(columns=column), (value, req)
        con.execute(query).fetchall()     
     else:
        query="UPDATE practice.proects SET {columns} = ? WHERE {columns} LIKE ?".format(columns=column),
        (value, '%' + req + '%')
        con.execute(query).fetchall()   


     tree_update()
# та самая функция, которая обновляет в приложении
def tree_update():
      global tree
      tree.place_forget()
      tree = ttk.Treeview(root, columns=columns, show='headings')
      tree.column('№', width=40)
      tree.column('Название', width=130)
      tree.column('Описание', width=130)
      tree.column('Статус', width=150)
      tree.column('Дата начала', width=180)
      tree.column('Дата завершения', width=180)
      tree.column('Навыки',width=130)
      tree.column('Видимость', width=90)

      conn = sq.connect('db.db')
      cursor = conn.cursor()
      data = cursor.execute("SELECT * FROM proects").fetchall()
      conn.close()
      for i in columns:
                    tree.heading(i, text=i)
      for i in data:
        tree.insert('', index=ttk.END, values=i)
      tree.place(x=400, y=60)

# функция которая ищет в таблице проекты по названию и\или описанию
def find_proj():
    name=entry_name.get()
    desc=entry_desc.get()
    conn = sq.connect('db.db')
    cursor = conn.cursor()
    
    if name and desc:
        cursor.execute("SELECT * FROM proects WHERE name LIKE ? AND description LIKE ?", ('%' + name + '%', '%' + desc + '%'))
    elif name: 
        cursor.execute("SELECT * FROM proects WHERE name LIKE ?", ('%' + name + '%',))
    elif desc:  
        cursor.execute("SELECT * FROM proects WHERE description LIKE ?", ('%' + desc + '%',))
    

    rows = cursor.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
  
    for row in rows:
        tree.insert('', index=ttk.END, values=row)

    tree.place(x=380, y=60)

# две функции, которые показывают\убирают табллицу


def save_proj():
        print('ff')
        # insert into db + ifelse проверка введенных данных

# фунуция которая изменяет участников
def edit_groups():
     clear()
     label_change.place(x=400,y=10)
     lab_find.place(x=160,y=250)
     ent_findman.place(x=160,y=300)
     ent_findman.insert(0, f'Имя\фамилия')
     btn_findman.place(x=160,y=350)
     lab_editman.place(x=160,y=490)
     lab_strman.place(x=400,y=490)
     comb_editman.place(x=160,y=530)
     comb_find.place(x=400,y=530)
     ent_valuesman.place(x=160,y=600)
     ent_insert.place(x=400,y=600)
     btn_editman.place(x=160,y=660)
     tree_stud.place(x=400, y=60)

def analyse():
     clear()

# def show_groups():
#      tree1.place(x=400,y=60)

# def close_groups():
#      tree1.place_forget()

btn_save = ttk.Button(root, text='Сохранить', command=save_update_proj,style='Outline.TButton')
btn_add = ttk.Button(root, text='Добавить', command=add_proj,style='Outline.TButton')
btn_add.place(x=10,y=50)

btn_plus= ttk.Button(root, text='  +  ', command=add,style='Outline.TButton')
btn_min= ttk.Button(root, text='  -  ', command=drop,style='Outline.TButton')

btn_edit= ttk.Button(root, text='Исправить проект', command=edit_proj,style='Outline.TButton')
btn_edit.place(x=10,y=100)

btn_find=ttk.Button(root, text='Найти проект', command=find_proj,style='Outline.TButton')
btn_snupd=ttk.Button(root, text='Изменить и обновить', command=save_and_update,style='Outline.TButton')
btn_edit_par=ttk.Button(root, text='Исправить участников', command=edit_groups,style='Outline.TButton')
btn_edit_par.place(x=10,y=150)
# btn_team=ttk.Button(root, text='Все команды', command=show_groups,style='Outline.TButton')
# btn_closeteam=ttk.Button(root, text='Закрыть таблицу', command=close_groups,style='Outline.TButton')


btn_findman=ttk.Button(root, text='Найти участника',style='Outline.TButton')
btn_editman=ttk.Button(root, text='Изменить и обновить',style='Outline.TButton')

btn_analyse=ttk.Button(root, text='Аналитика',style='Outline.TButton', command=analyse)
btn_analyse.place(x=10,y=200)

root.mainloop()