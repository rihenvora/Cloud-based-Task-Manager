import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from taskboarddb import *
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)


class addTask(webapp2.RequestHandler):
    #--------------------------------------------------
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url=''
        url_string=''
        list1=''
        listusr=''
        tskdb=''
        tskdb1=[]
        tskdb_key=''
        user = users.get_current_user()
        #list1=self.request.get('key').strip("Key()").split(",")
        list1=int(self.request.get('key'))
        list=[]
        listr=''
        if user:
            #Task Board
            tskdb_key = ndb.Key('TaskBoard',list1)
            taskdb = tskdb_key.get()
            #User
            tskdb_key1 = ndb.Key('User', user.user_id())
            taskdb1 = tskdb_key1.get()

            list.append(taskdb)
            for lst in list:
                for usr in lst.user:
                    #lst.user.remove(taskdb1.key)
                    tskdb1.append(usr.get())

            #tskdb1=User(email_address == user.email())
            listusr=User.query().fetch()
            #tskdb1=User(email_address=user.email())

            url=users.create_logout_url(self.request.uri)
            url_string='logout'
            #list1=eletronicvehicle
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
        'url':url,
        'url_string':url_string,
        'user' : user,
        'tskdb' : tskdb1,
        'tskdbid' : list1
        }

        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))
    #------------------------------------------------------------------

    def post(self):
        self.response.headers['Content-Type']='text/html'
        action = self.request.get('button')
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        taskdb = ''
        tskdb_key=''
        list = ''
        list1=[]
        keys=[]
        tskdbid=''
        # pull the current user from the request
        user = users.get_current_user()
        if action == 'Add':
            # determine if we have a user logged in or not
            tskdbid=self.request.get("hdnid")
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            tskdb_key = ndb.Key('TaskBoard',int(tskdbid))
            taskdb = tskdb_key.get()
            list1.append(taskdb)
            tsk_key = ndb.Key('Task',user.user_id())
            tsk = tsk_key.get()

            tsk = Task(
                taskname = self.request.get("name").strip(),
                due_date = datetime.strptime(self.request.get("date"), '%Y-%m-%d'),
                created_by = user.email(),
                taskboardid = tskdbid,
            )

            for task in list1:
                if len(task.task)>0:
                    for tsks in task.task:
                        keys.append(tsks.taskname)

            if len(keys)>0:
                if self.request.get("name").strip() not in keys:
                     tsk.put()
                     taskdb.taskids.append(str(tsk.key.id()))
                     taskdb.task.append(tsk)
                     taskdb.put()
            else:
                 tsk.put()
                 taskdb.taskids.append(str(tsk.key.id()))
                 taskdb.task.append(tsk)
                 taskdb.put()


            self.redirect('/taskboardDetails?key='+tskdbid)
        elif self.request.get('button') == 'Cancel':
            tskdbid=self.request.get("hdnid")
            self.redirect('/taskboardDetails?key='+tskdbid)
