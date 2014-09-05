#!/usr/bin/env python

import unittest
import task_manager
import datetime

class TaskManagerTaskAddingCase(unittest.TestCase):


    def date(self, timedelta_days = 0):
        """
        Returns the day relative to today (at 00:00)
        """

        return (datetime.date.today() + datetime.timedelta(days = timedelta_days)).strftime("%d%m%y")

    def clear_task_manager_state(function):
        """
        Decorator clears task_manager to by-pass auto-save for testing
        """

        def innerfunc(*args, **kwargs):
            self = args[0]

            self.task_manager.all_tasks = {}
            retval = function(*args, **kwargs)
            return function
        return innerfunc

    def setUp(self):
        self.task_manager = task_manager.TaskManagerFactory.make_task_manager()
        self.user = 'user'
        self.task = 'wash the dishes'

    @clear_task_manager_state
    def test_add_single_active_task(self):
        
        # Test that method returns a task
        self.assertEquals(self.task_manager.add_task(self.user, self.task, self.date(1)).__class__, task_manager.Task)
        # Test that there is one task and that it is active
        self.assertEquals(len(self.task_manager.get_all_tasks()), 1)
        self.assertEquals(len(self.task_manager.get_active_tasks()), 1)


    @clear_task_manager_state
    def test_add_active_tasks(self):
        
        # Test that method returns a task
        self.assertEquals(self.task_manager.add_task(self.user, self.task, self.date()).__class__, task_manager.Task)
        # Test that there is one task and that it is active
        self.assertEquals(len(self.task_manager.get_all_tasks()), 1)
        self.assertEquals(len(self.task_manager.get_active_tasks()), 1)
        self.assertEquals(self.task_manager.add_task(self.user, self.task, self.date(1)).__class__, task_manager.Task)
        self.assertEquals(len(self.task_manager.get_all_tasks()), 2)
        self.assertEquals(len(self.task_manager.get_active_tasks()), 2)

    @clear_task_manager_state
    def test_one_active_one_inactive_due_to_date(self):
        # add task due for today - active
        self.task_manager.add_task(self.user, self.task, self.date())
        # add task due for yesterday - inactive
        self.task_manager.add_task(self.user, self.task, self.date(-1))

        self.assertEquals(len(self.task_manager.get_all_tasks()), 2)
        self.assertEquals(len(self.task_manager.get_active_tasks()), 1)
        self.assertEquals(len(self.task_manager.get_old_tasks()), 1)

    @clear_task_manager_state
    def test_one_active_one_inactive_due_to_completion(self):
        # add task due for today - active
        self.task_manager.add_task(self.user, self.task, self.date())
        # add task due and mark it as complete - inactive
        t = self.task_manager.add_task(self.user, self.task, self.date())

        self.task_manager.complete_task(t.task_id)
        self.assertEquals(len(self.task_manager.get_all_tasks()), 2)
        self.assertEquals(len(self.task_manager.get_active_tasks()), 1)
        self.assertEquals(len(self.task_manager.get_old_tasks()), 1)

    @clear_task_manager_state
    def test_return_user_active_tasks(self):

        self.task_manager.add_task(self.user, self.task, self.date())
        self.task_manager.add_task(self.user, self.task, self.date())
        self.task_manager.add_task(self.user, self.task, self.date(-1))
        self.assertEquals(len(self.task_manager.get_user_tasks(self.user)), 2)

if __name__ == "__main__":

    unittest.main()
