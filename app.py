#!/usr/bin/env python
import flask
from flask import Flask

import token_parser
import task_manager
app = Flask(__name__)
TM = task_manager.TaskManagerFactory.make_task_manager()

@app.route("/tasks/", methods=['POST'])
def hello():
    
    data = flask.request.form
    tokens = "add_task:, my_tasks:, commands:, help:, task:, date:".split(', ')
    
    try:   
        if data['trigger_word'] == "add_task:":
            response = "Your task has been added"
            parsed_command = token_parser.parse_with_tokens(data['text'], tokens)
            new_task = TM.add_task(data['user_name'], parsed_command['task'], parsed_command['date'])
            response = "{0}\nTask id:{1} Task:{2}".format(response, new_task.task_id, new_task.task)

        elif data['trigger_word'] == "my_tasks:":
            user_tasks = TM.get_user_tasks(data['user_name'])
            print user_tasks
            if user_tasks is not None:
                response = "Your active tasks are:\n{0}".format("\n".join(user_tasks))
            else:
                response = "You do not have any active tasks"

        elif data['trigger_word'] == "commands:":
            response = 'add_task: task:task_description date:ddmmyy (Provide description and target date))\nmy_tasks: (shows tasks for user)'

        else:
            response = "Sorry, the command does not exist.\n{0}".format(response)
        
    except:
        response = "Sorry, an error occured. Did you forget a parameter? Did you remember to add spaces?"
    return flask.jsonify(text = response)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 9121, debug = True)
