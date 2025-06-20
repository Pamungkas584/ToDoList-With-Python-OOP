import json
from datetime import datetime
import copy

data = "C:/Users/pamun/program try/python/latihan/To do list/data.txt" # mengarahkan kemana data akan di simpan


class Node :
    
    id_node = 1 # id untuk setiap node yang di buat
    
    def __init__(self,filename=data):
        self.filename = filename
        self.load_id_from_file()
        self.tasks_id = Node.id_node
        self.next_tasks_id = None
        self.prev_tasks_id = None
        Node.id_node += 1 # id akan terus bertambah seiring node di buat
    
    def load_id_from_file(self):
        ''' Load id node terakhir'''
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                tasks = data.get('tasks', [])
                
                if tasks: # ambil task id yang paling besar
                    max_id = max(task['tasks_id'] for task in tasks)
                    Node.id_node = max_id + 1
                else:
                    Node.id_node = 1
        except:
            Node.id_node = 1
            


class ToDoList :
    
    
    def __init__(self,filename = data):
        self.filename = filename
        self.tasks = []     
        self.history_stack = []
        self.redo_stack= []
        self.complete_tasks = []
        self.load_from_file()
        self.save_to_file()
    
    def add_tasks(self,new_task,priority,deadline,node_task) :
        ''' add task '''
        

        if len(self.tasks) >= 1 : # mencegah agar tidak melakukan loop jika task masih kosong
            for item in self.tasks: 
                if item['next_tasks_id'] == None : # mencari node mana yang memiliki next None(tail)
                    item['next_tasks_id'] = node_task.tasks_id # membuat node yang baru di tambahkan sebagai next node dari tail
                    node_task.prev_tasks_id = item['tasks_id'] # membuat node tail sebagai preview dari node baru
            
        self.tasks.append({
            'tasks_id' : node_task.tasks_id,
            'next_tasks_id' : node_task.next_tasks_id,
            'prev_tasks_id' : node_task.prev_tasks_id,
            "task" : new_task,
            "priority" : priority,
            "deadline" : deadline
        })
        
        self.history_stack.append({
            'action' : "add",
            'tasks_id' : node_task.tasks_id,
            'next_tasks_id' : node_task.next_tasks_id,
            'prev_tasks_id' : node_task.prev_tasks_id,
            "task" : new_task,
            "priority" : priority,
            "deadline" : deadline
        })

        self.save_to_file()


    def save_to_file(self):
        ''' menyimpan data '''
        data = {
            'tasks_complete' : self.complete_tasks,
            'tasks': self.tasks,
            'history': self.history_stack,
            'redo_stack': self.redo_stack
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        '''mengambil data dari file txt'''
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', [])
                self.history_stack = data.get('history', [])
                self.redo_stack = data.get('redo_stack', [])
                self.complete_tasks = data.get('tasks_complete', [])
        except:
            self.complete_tasks = []
            self.tasks = []
            self.history_stack = []
            self.redo_stack = []

    def sorted_tasks(self) :
        ''' sorted berdasarkan priority '''
        self.load_from_file()
        return sorted(self.tasks, key=lambda x: x['priority'])

    def get_indexs(self,id_target) :
        ''' looping untuk mendapatkan index berdasarkan key'''
        for index,task in enumerate(self.tasks) :
            if task['tasks_id'] == id_target:
                return index
    
    def remove_tasks(self,index_target,is_undo=False) :
        ''' menghapus tugas '''
        target = self.tasks[index_target]
        
        if not is_undo : # mengecek apakah fungsi di panggil dari undo atau tidak | akan berjalan jika fungsi tidak di panggil dari undo
            self.tasks[index_target]['action'] = "remove" # menandai action apa yang di lakukan ketika undo nanti
            self.history_stack.append(self.tasks[index_target])
        
        del self.tasks[index_target]
        self.save_to_file()
        self.connect(target,mode="remove") 
        self.rebuild_squance()
    
    def connect(self,target,mode) : 
        ''' menghubungkan node ketika terjadi perubahan data '''
        for task in self.tasks :
            
            if mode == "remove" :
                if task['next_tasks_id'] == target['tasks_id'] :
                    task['next_tasks_id'] = target['next_tasks_id'] # menghubungkan sisa elemen ketika elemen di antaranya di ambil
                
                if task['prev_tasks_id'] == target['tasks_id'] :
                    task['prev_tasks_id'] = target['prev_tasks_id'] # ini juga 
                
                if task['next_tasks_id'] == None and target['prev_tasks_id'] == task['tasks_id'] : # jika next_tasks dari task kosong dan prev_tasks dari target adalah task maka akan menjadikan target tail
                    task['next_tasks_id'] = target['tasks_id']
            
            elif mode == 'add': 
                if task['tasks_id'] == target['prev_tasks_id']:
                    task['next_tasks_id'] = target['tasks_id']
                if task['tasks_id'] == target['next_tasks_id']:
                    task['prev_tasks_id'] = target['tasks_id']
            
        self.save_to_file()
    
    def rebuild_squance(self) : 
        ''' mengurutkan data berdasarkan node '''
        mapping = {}
        squance_data = []
        head = None # menjaga ketika head tidak di temukan
        
        for task in self.tasks : 
            mapping[task['tasks_id']] = task
            if task['prev_tasks_id'] is None :
                head = task
        
        while head != None : 
            squance_data.append(head)
            next_tasks_id = head['next_tasks_id']
            head = mapping.get(next_tasks_id)

        
        self.tasks = squance_data
        self.save_to_file()
    
    def undo(self) :
        ''' melakukan undo '''
        try :
            task = self.history_stack.pop()
            self.redo_stack.append(copy.deepcopy(task)) # menambahkan elemen yang di undo ke dalam histori redo
            
            if task['action'] == 'add' : # jika actionnya adlah add maka undo adalah remove
                self.remove_tasks(-1,is_undo=True)
            
            elif task['action'] == 'remove' : # jika actionnya adlah remove maka undo adalah add
                del task['action'] # menghapus key action dan valuenya
                self.tasks.append(task) #menambahkan datanya kembali ke dalam task
                self.connect(task,mode="add")
            
            elif task['action'] == 'complete':
                del task['action'] # Undo tugas yang sudah diselesaikan
                self.tasks.append(task)
                self.connect(task, mode='add')


                self.complete_tasks = [
                    t for t in self.complete_tasks if t['tasks_id'] != task['tasks_id']  # Hapus dari daftar tugas yang selesai
                ]
            
            
            self.rebuild_squance() 
            
        except :
            print("TIdak ada tugas yang bisa di undo!")
    
    def redo(self):
        ''' melakukan redo '''
        try :
            task = self.redo_stack.pop()
            self.history_stack.append(copy.deepcopy(task)) # mengembalikan elemen redo ke undo
            
            if task['action'] == 'remove' : # jika actionnya remove maka redonya juga remove
                # redo tugas yang sebelumnya di tambahkan
                index_target = self.get_indexs(task["tasks_id"])
                self.remove_tasks(index_target,is_undo=True)
                
                
                
            
            elif task['action'] == 'add' : # jika actionnya add maka redonya juga add
                #redo tugas yang sebelumnya di hapus
                del task['action'] # menghapus key action dan valuenya sebelum di tambahkan ke daftar tasks
                self.tasks.append(task) # menambahkan kembali datanya ke dalam task
                
                self.connect(task,mode="add")
            
            elif task['action'] == 'complete':
                # Redo tugas selesai
                self.complete_tasks.append(task)
                index_target = self.get_indexs(task["tasks_id"])
                self.remove_tasks(index_target, is_undo=True)
            

            self.rebuild_squance()
        except :
            self.redo_stack = [] #mencegah agar stack redo tidak ada duplikasi
            self.save_to_file()
            print("tidak ada tugas yang bisa di redo!")
    
    def complete(self,id_target) :
        ''' menandai tugas selesai '''
        index_target = self.get_indexs(id_target)
        task_complete = self.tasks[index_target]
        
        task_complete['action'] = 'complete'
        self.history_stack.append(copy.deepcopy(task_complete))

        self.complete_tasks.append(task_complete)
        self.remove_tasks(index_target, is_undo=True)  # Jangan simpan lagi ke history
        self.save_to_file() 
    
    def get_complete_tasks(self) :
        '''' getter daftar tugas selesai '''
        return self.complete_tasks