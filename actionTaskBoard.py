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


class actionTaskBoard(webapp2.RequestHandler):
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
        taskd=[]
        userd=[]
        utaskb=[]
        utaska=[]
        tsklist=[]
        utaskbd=[]
        ut=''
        user = users.get_current_user()
        #list1=self.request.get('key').strip("Key()").split(",")
        list1=int(self.request.get('key1'))
        actionperform =self.request.get('key2')
        if actionperform == 'remove':
            userid=self.request.get('key')
            #Taskboard
            tskdb_key = ndb.Key('TaskBoard',int(list1))
            taskdb = tskdb_key.get()
            #user
            user_key = ndb.Key('User',int(userid))
            user = user_key.get()
            utaskb=user.taskassigned

            for task in taskdb.user:
                if task != user.key:
                    taskd.append(task) #taskboard after removal user
            taskdb.user = taskd
            taskdb.put()
            #changing Status Of task assigned
            for task in taskdb.task:
                if task.taskname in utaskb:
                    tsklist.append(str(task.taskname))
                    task.assignstatus = 2
            taskdb.put()


            for tkbd in user.taskboard:
                if str(tkbd) != str(list1):
                    utaskbd.append(tkbd) #user after removal TaskBoard
                user.taskboard = utaskbd
                user.put()

            for tkbd in user.taskassigned:
                if str(tkbd) not in str(tsklist):
                     utaska.append(utb) #user after removal TaskBoard
                user.taskassigned = utaska
                user.put()


            self.redirect('/taskboardDetails?key='+str(list1))
        elif actionperform == 'delete':
            tskdb_key = ndb.Key('TaskBoard',int(list1))
            taskdb = tskdb_key.get()
            byebye=[]
            if len(taskdb.task)==0 and len(taskdb.user)==1:
                users1=ndb.Key('User',taskdb.user_id).get()
                for utb in users1.taskboard:
                    if str(utb) != str(list1):
                        byebye.append(utb)
                users1.taskboard=byebye
                users1.put()
                tskdb_key.delete()
                self.redirect('/')
            else:
                self.redirect('/')

        elif actionperform == 'edit':
            list=[]
            listr=''
            if user:
                #Task Board
                tskdb_key = ndb.Key('TaskBoard',list1)
                taskdb = tskdb_key.get()
                list.append(taskdb)
                url=users.create_logout_url(self.request.uri)
                url_string='logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            template_values = {
            'url':url,
            'url_string':url_string,
            'user' : user,
            'tskdbid' : list1,
            'taskboard' : list,
            }

            template = JINJA_ENVIRONMENT.get_template('actionTaskBoard.html')
            self.response.write(template.render(template_values))
    #-----------------------------------------------------------------
    def post(self):
        self.response.headers['Content-Type']='text/html'
        action = self.request.get('button')
        # pull the current user from the request
        user = users.get_current_user()
        tskdbid=''
        if action == 'Edit':
            # determine if we have a user logged in or not
            tskdbid=self.request.get("hdnid").strip()
            tskdb_key = ndb.Key('TaskBoard',int(tskdbid))
            taskdb = tskdb_key.get()
            taskboards=[]
            taskboardname=[]
            #taskboards.append(tskdb1.taskboard)
            query=User.query().fetch()

            for qry in query:
                taskboards.append(qry.taskboard)

            for tbname in taskboards:
                for tb in tbname:
                    tskdb_key1 = ndb.Key('TaskBoard', int(tb))
                    tskdb2 = tskdb_key1.get()
                    taskboardname.append(str(tskdb2.taskboardname))

            if self.request.get('name') not in taskboardname:
                taskdb.taskboardname = self.request.get("name")
                taskdb.put()
            self.redirect('/taskboardDetails?key='+tskdbid)
        elif self.request.get('button') == 'Cancel':
            tskdbid=self.request.get("hdnid").strip()
            self.redirect('/taskboardDetails?key='+tskdbid)
