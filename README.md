# TODO list application - REST api using Flask-RESTful

## Table of contents

- [About](#about)
- [How to run the application?](#how-to-run-the-application)

## About

API to a TODO List application.

In place of a database we will store our task list in a memory structure. This will only work when the web server that runs our application is single process and single threaded. This is OK for Flask's own development web server. It is not OK to use this technique on a production web server, for that a proper database setup must be used.

Each entry in the array has the following fields:

- **id:** unique identifier for tasks. Numeric type.
- **title:** short task description. String type.
- **description:** long task description. Text type.
- **done:** task completion state. Boolean type.

The tasks resource use HTTP methods as follows:

| HTTP method |	URI | Example | Action |
| ----------- | --- | ------- | ------ |
| **GET** | http://[hostname]/todo/api/v1.0/tasks | ```curl -i http://localhost:5000/todo/api/v1.0/tasks -u user1:password``` | Retrieve list of tasks |
| **GET** | http://[hostname]/todo/api/v1.0/tasks/[task_id] -u user1:password | ```curl -i http://localhost:5000/todo/api/v1.0/tasks/1 -u user1:password``` | Retrieve a task |
| **POST** | http://[hostname]/todo/api/v1.0/tasks -u user1:password | ```curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks -u user1:password ``` | Create a new task |
| **PUT** | http://[hostname]/todo/api/v1.0/tasks/[task_id] | ```curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2 -u user1:password``` | Update an existing task |
| **DELETE** | http://[hostname]/todo/api/v1.0/tasks/[task_id] | ```curl -X DELETE http://localhost:5000/todo/api/v1.0/tasks/2 -u user1:password``` | Delete a task |

## How to run the application

1. Install [virtualenv](https://virtualenv.pypa.io/en/latest/) and [Flask](https://palletsprojects.com/p/flask/)
	* To activate the virtualenv on Linux or MacOS: ```source venv/bin/activate```
	* To activate the virtualenv on Windows: ```\venv\Script\activate.bat```

2. Run the application

Step-by-step:

```sh
cd flask_todo_app_rest_api-using_flask_restful/

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python app.py
```

**Note**: To desactivate the virtual environment

```sh
deactivate
```