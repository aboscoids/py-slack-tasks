#!/usr/bin/env python

import datetime
import jsonpickle
import os
import tempfile

class TaskManagerFactory(object):

    def make_task_manager():
        if os.path.exists('tasks.tsk'):
            f = open('tasks.tsk', 'r')
            loaded = jsonpickle.decode(f.read())
            f.close()
            return loaded
        else:
            return TaskManager()
    make_task_manager = staticmethod(make_task_manager)


class Task(object):
    _task_id = 0
    def __init__ (self, user, task, date):
        self.user = user
        self.task = task
        self.is_completed = False
        # date in format ddmmyy
        self.date = (datetime.datetime.strptime(date, "%d%m%y")).date()
        
        self.task_id = Task._task_id
        Task._task_id += 1

    def is_active(self):
        return True if (self.date >= datetime.date.today() and self.is_completed is False ) else False

    def time_remaining(self):
        if self.is_active() is False:
            return None
        else:
            self.date - datetime.date.today()

    def complete(self):
        self.is_completed = True
    
    def __repr__(self):
        return "id: {0}, due: {1}, user: {2}, task: {3}".format(self.task_id, self.date, self.user, self.task)


class TaskManager(object):


    def save_state(function):
        def inner(*args, **kwargs):
            self = args[0]
            retval = function(*args, **kwargs)
            f = open('tasks.tsk', 'w')
            f.write(jsonpickle.encode(self))
            f.close()
            return retval
        return inner



    def __init__(self):
        
        self.all_tasks = {}


    @save_state
    def add_task(self, user, task, date):
        t = Task(user, task, date)
        self.all_tasks[t.task_id]=t
        return t

    @save_state
    def complete_task(self, task_id):
        self.get_task(task_id).complete()

    def get_task(self, task_id):
        return self.all_tasks[task_id]
    def get_active_tasks(self):

        return [ task for task in self.get_all_tasks() if task.is_active() ]

    def get_all_tasks(self):

        return [task for id, task in self.all_tasks.iteritems()]

    def get_old_tasks(self):

        return [task for task in self.get_all_tasks() if task not in self.get_active_tasks()]
    
    def get_user_tasks(self, user_name):
        tasks = []
        for t in self.get_active_tasks():

            if t.user == user_name:
                tasks.append(str(t))
        return tasks if len(tasks)>0 else None


