import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import urlparse

from taskboarddb import *
from add import AddTB
from taskboardDetails import taskboardDetails
from addTask import addTask
from assignTask import assignTask
from actionTask import actionTask
from actionTaskBoard import actionTaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        tskdb = ''
        list = ''
        list1=''
        user=''
        keys=[]
        tskdbid=''
        usrid=''
        taskboard=''
        # pull the current user from the request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            query = User.query(User.email_address == user.email()).get() #Query To GetUser Email Address

            if tskdb == '' and query == None:
                welcome = 'Welcome to  the Application'
                tskdb_key = ndb.Key('User', user.user_id())
                taskdb = tskdb_key.get()
                tskdb = User(id=user.user_id())
                tskdb = User(email_address=user.email())
                tskdb.put()

                list = User.query(User.email_address == user.email()).fetch()


            else:
                welcome = 'Welcome Back'
                tskdb = User(email_address=user.email())
                list = User.query(User.email_address == user.email()).fetch()

                for tb in list:
                    for tbi in tb.taskboard:
                        #temp=tbi.strip("Key(),")
                        #keys.append(tbi)
                        # keys1=[ndb.Key('TaskBoard',int(tbi) )
                        #         for usrid in tb.taskboard ]
                        keys1=ndb.Key('TaskBoard',int(tbi)).get()
                        #tskdbid=ndb.get_multi(keys1)
                        keys.append(keys1)


        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'tskdb' : tskdb,
            'showList' : list,
            'showTaskB' : keys,
            'keylen' : len(keys)
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type']='text/html'
        action = self.request.get('button')
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        tskdb = ''
        tskdb_key=''
        list = ''
        list1=''
        keys=[]
        # pull the current user from the request
        user = users.get_current_user()
        if action == 'Add':
            # determine if we have a user logged in or not
            if user:
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'
                #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
                tskdb_key = ndb.Key('User', int(self.request.get('hdnid')))
                tskdb = tskdb_key.get()
                tskdb.name = self.request.get('name').strip()
                tskdb.put()
                list = User.query(User.email_address == user.email()).fetch()

                for tb in list:
                    for tbi in tb.taskboard:
                        #temp=tbi.strip("Key(),")
                        #keys.append(tbi)
                        # keys1=[ndb.Key('TaskBoard',int(tbi) )
                        #         for usrid in tb.taskboard ]
                        keys1=ndb.Key('TaskBoard',int(tbi)).get()
                        #tskdbid=ndb.get_multi(keys1)
                        list.append(keys1)
                        keys.append(keys1)
                #list1 = TaskBoard.query(TaskBoard.created_by == user.email()).fetch()

            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'tskdb' : tskdb,
            'showList' : list,
            'showTaskB' : keys,
            'keylen' : len(keys)
        }
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        #template = JINJA_ENVIRONMENT.get_template('addEVDetails.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', AddTB),
    ('/taskboardDetails', taskboardDetails),
    ('/addTask', addTask),
    ('/assignTask', assignTask),
    ('/actionTask', actionTask),
    ('/actionTaskBoard', actionTaskBoard),
], debug=True)
