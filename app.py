from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
	if username == 'user1':
		return 'password'
	return None


@auth.error_handler
def unauthorized():
	'''
	return 403 instead of 401 to prevent browsers from displaying the default
	auth dialog
	'''
	return make_response(jsonify({'message': 'Unauthorized access'}), 403)


tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit',
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web',
		'done': False
	}
]


task_fields = {
	'title': fields.String,
	'description': fields.String,
	'done': fields.Boolean,
	'uri': fields.Url('task')
}


'''
Flask-RESTful provides a Resource base class that can define the routing for one or more HTTP methods 
for a given URL. For example, you can define a resource with GET, PUT and DELETE methods.
'''
class TaskListAPI(Resource):
	'''
	The routes in the REST server are all protected with HTTP basic authentication. 
	This code uses the decorator provided by the Flask-HTTPAuth extension.

	Since the Resouce class inherits from Flask's MethodView, it is possible to attach decorators to 
	the methods by defining a decorators class variable.
	'''
	decorators = [auth.login_required]

	def __init__(self):
		'''
		Flask-RESTful provides the RequestParser class to handle validation of data given with the request. 
		This class works in a similar way as argparse for command line arguments.

		One benefit of letting Flask-RESTful do the validation is that there is no need to have a handler 
		for the bad request code 400 error, this is all taken care of by the extension.
		'''
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, required=True,
			help='No task title provided',
			location='json')
		self.reqparse.add_argument('description', type=str, default="",
			location='json')
		super(TaskListAPI, self).__init__()

	'''
	Flask-RESTful automatically handles the conversion to JSON, so instead of this:
		return jsonify( { 'task': make_public_task(task) } )
	You can do this:
		return { 'task': make_public_task(task) }

	The make_public_task wrapper from the original server converted a task from its internal 
	representation to the external representation that clients expected. 
	The conversion included removing the id field and adding a uri field in its place. 
	Flask-RESTful provides a helper function to do this in a much more elegant way that not 
	only generates the uri but also does type conversion on the remaining fields.

	The task_fields structure serves as a template for the marshal function. 
	The fields.Url type is a special type that generates a URL. 
	The argument it takes is the endpoint (recall that I have used explicit endpoints when 
	I registered the resources specifically so that I can refer to them when needed).
	'''
	def get(self):
		return {'tasks': [marshal(task, task_fields) for task in tasks]}

	def post(self):
		args = self.reqparse.parse_args()
		task = {
			'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
			'title': args['title'],
			'description': args['description'],
			'done': False
		}
		tasks.append(task)
		'''
		Flask-RESTful also supports passing a custom status code back when necessary (e.g. 201 code)
		'''
		return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):
	decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, location='json')
		self.reqparse.add_argument('description', type=str, location='json')
		self.reqparse.add_argument('done', type=bool, location='json')
		super(TaskAPI, self).__init__()

	def get(self, id):
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		return {'task': marshal(task[0], task_fields)}

	def put(self, id):
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		task = task[0]
		args = self.reqparse.parse_args()
		for k, v in args.items():
			if v is not None:
				task[k] = v
		return {'task': marshal(task, task_fields)}

	def delete(self, id):
		task = [task for task in tasks if task['id'] == id]
		if len(task) == 0:
			abort(404)
		tasks.remove(task[0])
		return {'result': True}


'''
The add_resource function registers the routes with the framework using the given endpoint. 
If an endpoint is not given then Flask-RESTful generates one for you from the class name, 
but since sometimes the endpoint is needed for functions such as url_for I prefer to make it explicit.
'''
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')

if __name__ == '__main__':
	app.run(debug=True)
