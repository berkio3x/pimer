from tkinter import *
from tkinter import ttk, Button
from datetime import datetime, timedelta
from functools import partial 
import uuid 

tasks = []

import enum

class TaksStatus(enum.Enum):
    active= 'active'
    paused= 'paused'

class App:
    def __init__(self, w, h):
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
      
        self.root.geometry(f'{w}x{h}' )

        self.tasks = {}
        self.task_status_button_map = {}
        self.task_time_label_map = {}

    def get_task_len(self):
        """Return length of active tasks"""
        return len(self.tasks.keys())
        
    def create_task(self, ):
        pass

    def pause_task(self, b):
        b.configure(bg='orange')

    def gen_task(self, text):
        task_id = uuid.uuid4().hex
        start_time = datetime.now()
        return {
            'text': text,
            'status':TaksStatus.active,
            'start_time':start_time,
            'time_spent': (start_time + timedelta(seconds=1)),
            'task_id': task_id
        }

    def get_task_info(self, task_id):
        return self.tasks[task_id]
    
    def update_task_time_spent(self, task_id):
        task = self.get_task_info(task_id)
        task['time_spent'] += datetime.now() - task['start_time']

        time_spent_label = self.task_time_label_map[task_id]
        time_spent_label.configure(text=task['time_spent'].time())

    def link_task_status_button_to_task(self, task_id, b):
        self.task_status_button_map[task_id] = b

    def save_task(self, task):
        self.tasks[task['task_id']] = task

    def get_task_status(self, task_id):
        return self.tasks[task_id]['status']

    def mark_button_active(self, b):
        b.configure(bg='lightgreen')
    
    def mark_button_paused(self, b):
        b.configure(bg='orange')

    def toggle_task_status(self, task_id, button):
        task_status = self.get_task_status(task_id)
        if task_status == TaksStatus.active:
            self.tasks[task_id]['status'] =  TaksStatus.paused
            self.mark_button_paused(button)
            self.update_task_time_spent(task_id)
        else:
            self.tasks[task_id]['status'] =  TaksStatus.active
            self.mark_button_active(button)

    def create_task_status_button(self, frame):
        b = Button(frame, text='⏺', 
            height=1,
            width=2, 
            bg='#6ce186',
            
        )
        return b

    def create_task_time_spent_label(self, frame):
        l = ttk.Label(frame, text='time spend', background='beige')
        return l

    def add_task_status_button_action(self, task_id):
        b = self.task_status_button_map[task_id]
        print(self.task_status_button_map,"===>")
        b.configure(command=partial(
            self.toggle_task_status,
            task_id,  
            b)
        )

    def create_task_label(self, frame, text):
 
        return Label(frame, text=text)

    def create_task_input_ui(self):

        self.e = Entry(self.root ,text='Task')
        self.e.focus_set()
        self.e.grid(row=2,column=1)
        self.task_create_button = Button(
            self.root,text='create task',
            command=self.create_task
        )
        self.task_create_button.grid(row=2,column=2)  

    def create_task_list_holder_ui(self):
        self.tasks_frame =  ttk.Frame(self.root, padding=10)
        self.tasks_frame.grid(row=3, column=1) 

    def create_task(self):
        """
        Main method used to create ui widgets 
        for a task & place it in ui.
        """
        text = self.e.get()
        # text = f'{text} - {datetime.now()}'

        task = self.gen_task(text)
        
        task_label = self.create_task_label(
            self.tasks_frame, 
            text)

        task_status_button = self.create_task_status_button(
            self.tasks_frame,
        )

        time_spent_label = self.create_task_time_spent_label(
            self.tasks_frame
        )

        
        self.link_task_status_button_to_task(
            task['task_id'],
            task_status_button
        )

        self.task_time_label_map[task['task_id']] = time_spent_label 
        self.add_task_status_button_action(
            task['task_id']
            )

        self.do_placement(
            [task_label, task_status_button ,time_spent_label]
        )

        self.save_task(task)


    def do_placement(self, task_widgets):
        """Place task widget in UI at appropriate place.
        CHnage this method to perfom some other kind of placements.
        """
        column = 0
        for _task_widget in task_widgets:
            task_count = self.get_task_len()
            print(column, _task_widget, "-==>")
            _task_widget.grid(row=task_count, column=column)
            column += 1

        
    def create_ui(self):
        """Create ui widgets to render information
        """
        self.create_task_input_ui()
        self.create_task_list_holder_ui()

    def start(self):
        """Boot ui & start application"""
        self.create_ui()
        self.root.mainloop()



if __name__ == '__main__':
    app = App(500, 600)
    app.start()
