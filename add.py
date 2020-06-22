import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from taskboarddb import *


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)



class AddTB(webapp2.RequestHandler):
	#--------------------------------------------------
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		url=''
		url_string=''
		tskdb=''
		list=''
		user = users.get_current_user()

		if user:
			tskdb_key = ndb.Key('User', user.user_id())
			tskdb = tskdb_key.get()
			tskdb=User(email_address=user.email())
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			list = User.query(User.email_address == user.email()).fetch()
		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		template_values = {
			'url':url,
			'url_string':url_string,
			'user' :list,
            'tskdb' : tskdb
		}


		template = JINJA_ENVIRONMENT.get_template('addTaskBoard.html')
		self.response.write(template.render(template_values))
	#------------------------------------------------------------------


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Add':
			user = users.get_current_user()
			userid=''
			tskdb=''
			tskdb1=''
			taskboards=[]
			taskboardname=[]
			if user:
				userid = int(self.request.get('hdnid').strip())
				tskdb_key = ndb.Key('TaskBoard', userid)
				tskdb = tskdb_key.get()

				tskdb_key1 = ndb.Key('User', userid)
				tskdb1 = tskdb_key1.get()
				#tskdb1 = User(email_address = user.email())

				tskdb = TaskBoard (
					taskboardname = self.request.get('name').strip(),
					created_by = user.email(),
					user_id = userid,
					user = [tskdb1.key]
				)
				taskboards.append(tskdb1.taskboard)
				query=User.query(User.email_address != user.email()).fetch()

				for qry in query:
					taskboards.append(qry.taskboard)

				for tbname in taskboards:
					for tb in tbname:
						tskdb_key1 = ndb.Key('TaskBoard', int(tb))
						tskdb2 = tskdb_key1.get()
						taskboardname.append(str(tskdb2.taskboardname))
				#query = tskdb.all().filter("email_address="user.email()).filter("name=",self.request.get('name')).filter("manufacturer=",self.request.get('manufacturer')).filter("year=",self.request.get('year'))
				#query=User.query(ndb.AND(User.email_address==user.email(),User.name==tskdb.name,User.manufacturer==tskdb.manufacturer,User.year==tskdb.year))
				#query=TaskBoard.query(TaskBoard.taskboardname==self.request.get('name'))
				if self.request.get('name') not in taskboardname:
					welcome="Details Entered"
					tskdb.put()
					tskdb1.taskboard.append(str(tskdb.key.id()))
					tskdb1.put()
				else:
					#Code to display error box to user Using Ctypes Library Which Comes with Python Installation
					print("Details Found")
			self.redirect('/')
		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
