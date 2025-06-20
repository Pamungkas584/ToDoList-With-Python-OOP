import os
from class_todo import ToDoList
from class_todo import Node
import datetime
import random
import string

def welcome_menu() : 
    os.system("cls")
    print("="*20)
    print(f"{"TO DO LIST":^20}")
    print("="*20)
    
    print("Pilih menu yang ingin di gunakan :")
    print("1.Tampilkan semua Tugas")
    print("2.Tambah tugas")
    print("3.Hapus tugas")
    print("4.Tandai Selesai")
    print("5.Undo ")
    print("6.Redo")
    print("7.Lihat Reminder")
    print("8.Lihat Tugas Selesai")
    print("9.keluar")


def show_task_header() :
    '''Head untuk show task'''
    print("\n"+ "="*120)
    print(f"{"NO":<5} | {"TUGAS":<40} | {"PRIORITY":<20} | {"SISA WAKTU":<20} | {"DEADLINE":<5}")
    print("-"*120)  

def show_task(todo_obj) :
    ''' looping show task '''
    show_task_header()
    sorted_task = todo_obj.sorted_tasks()
    for i, task in enumerate(sorted_task, 1):
        if task['priority'] == 1 :
            priority_new = "URGENT"
        elif task['priority'] == 2:
            priority_new = "HIGH"
        elif task['priority'] == 3 :
            priority_new = "MEDIUM"
        elif task['priority'] == 4 :
            priority_new = "LOW"
            
        
        deadline_date = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d")
        today = datetime.date.today()
        
        sisa_waktu = (deadline_date.date() - today).days
        
        if sisa_waktu > 0 :
            status = f"{sisa_waktu} Hari"
        elif sisa_waktu == 0 :
            status = f"Hari Ini"
        elif sisa_waktu < 0 :
            status = f"Terlambat {abs(sisa_waktu)} Hari"
            
            
        print(f"{i:<5} | {task['task']:<40} | {priority_new:<20} | {status:<20} | {task['deadline']:<5}")


def add_task_style() :
    os.system("cls")
    print("="*20)
    print(f"{"ADD TASK":^20}")
    print("="*20)

def add_task_confirm(new_task,priority,deadline):
    ''' view konfirmasi task '''
    add_task_style()
    print("Konfirmasi Tugas Anda")
    print(f"{'Nama Tugas : ':<20}{new_task}")
    print(f"{'Priority : ':<20}{priority}")
    print(f"{'Deadlinas : ':<20}{deadline}")

def remove_task(todo_obj) :
    ''' Hapus tugas '''
    show_task(todo_obj)
    while True:
        try :
            remove_index = int(input("Masukkan Nomor tugas : "))
            if remove_index > len(to.sorted_tasks()) :
                print("Item tidak di temukan")
                continue
            id_target = todo_obj.sorted_tasks()[remove_index - 1]['tasks_id']
            todo_obj.remove_tasks(todo_obj.get_indexs(id_target))
            break
        except ValueError :
            print("Masukkan index dengan benar")
            continue

def complete_task(todo_obj) :
    ''' tandai tugas selesai '''
    show_task(todo_obj)
    while True:
        try :
            complete_number = int(input("Masukkan Nomor tugas : "))
            if complete_number > len(todo_obj.sorted_tasks()) or complete_number <= 0 :
                print("Item tidak di temukan")
                continue
            id_target = todo_obj.sorted_tasks()[complete_number- 1]['tasks_id']
            todo_obj.complete(id_target)
            break
        except ValueError :
            print("Masukkan nomor dengan benar")
            continue




def add_task(todo_obj) :
    ''' Menambahkan Tugas '''
    node_task = Node()
    
    while True :
        add_task_style()
        
        
        new_task = input(f'{"Masukkan nama Tugas :":<20}')
        while True: #cek apakah priority valid
            try:
                priority = int(input("Masukkan urutan prioritas (1.Urgent / 2.High / 3.medium/ 4.Low)> "))
                if 1 <= priority <= 4:
                    break
                else:
                    print("Masukkan angka 1, 2, 3, atau 4!")
            except ValueError:
                print("Masukkan hanya angka, bukan huruf atau simbol!")
                
        while True : # cek apakah deadline valid
            try :
                tanggal = int(input(f"{'masukkan tanggal :':<20}"))
                bulan = int(input(f"{'masukkan Bulan :':<20}"))
                tahun = int(input(f"{'masukkan Tahun :':<20}"))
                deadline_date = datetime.date(tahun, bulan, tanggal)
                
                today = datetime.date.today()
                sisawaktu = (deadline_date - today).days

                if sisawaktu <= 0 :
                    print("Waktu yang kamu buat sudah lewat dari hari ini!")
                    continue
                
                deadline = deadline_date.strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Masukkan Deadline dengan benar!")
                continue
        
        add_task_confirm(new_task,priority,deadline)
        
        confirm = input("benar(y/n)> ")
        if confirm.lower() == 'y' :
            
            todo_obj.add_tasks(new_task,priority,deadline,node_task)
            
            break
        else :
            continue

def undo(todo_obj) :
    todo_obj.undo()

def redo(todo_obj) :
    todo_obj.redo()

def reminder(todo_obj):
    '' 'tugas dalam 3 hari '''
    show_task_header()
    sorted_task = todo_obj.sorted_tasks()
    for i, task in enumerate(sorted_task, 1):
        if task['priority'] == 1 :
            priority_new = "URGENT"
        elif task['priority'] == 2:
            priority_new = "high"
        elif task['priority'] == 3 :
            priority_new = "medium"
        elif task['priority'] == 4 :
            priority_new = "low"
            
        
        deadline_date = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d")
        today = datetime.date.today()
        
        sisa_waktu = (deadline_date.date() - today).days
        if  sisa_waktu <= 3 and sisa_waktu > 0 :
            sisa_waktu_str = f"{sisa_waktu} Hari"
            print(f"{i:<5} | {task['task']:<40} | {priority_new:<20} | {sisa_waktu_str:<20} | {task['deadline']:<5}")

def show_complete_task(todo_obj) :
    tasks_complete = todo_obj.get_complete_tasks()
    print("\n"+ "="*120)
    print(f"{"NO":<5} | {"TUGAS":<40} | {"PRIORITY":<20} | {"STATUS":<20} | {"DEADLINE":<5}")
    print("-"*120) 
    
    for i,task in enumerate(tasks_complete,1) :
        print(f"{i:<5} | {task["task"]:<40} | {task["priority"]:<20} | {"SELESAI":<20} | {task["deadline"]:<5}")
