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


class assignTask(webapp2.RequestHandler):
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
        user = users.get_current_user()
        #list1=self.request.get('key').strip("Key()").split(",")
        list1=int(self.request.get('key'))
        taskname=self.request.get('key1')
        list=[]
        listr=''
        if user:
            #Task Board
            tskdb_key = ndb.Key('TaskBoard',list1)
            taskdb = tskdb_key.get()

            list.append(taskdb)
            for lst in list:
                for usr in lst.user:
                    tskdb1.append(usr.get())
                for task in lst.task:
                    if taskname == task.taskname:
                        taskd.append(task)



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
        'tskdbid' : list1,
        'task' : taskd,
        'taskboard' : list,
        'taskname' : taskname
        }

        template = JINJA_ENVIRONMENT.get_template('assignTask.html')
        self.response.write(template.render(template_values))
    #-----------------------------------------------------------------
    def post(self):
        self.response.headers['Content-Type']='text/html'
        action = self.request.get('button')
        # pull the current user from the request
        user = users.get_current_user()
        if action == 'Assign':
            # determine if we have a user logged in or not
            tskdbid=self.request.get("hdnid").strip()
            taskname=self.request.get("hdntask").strip()
            tskdb_key = ndb.Key('TaskBoard',int(tskdbid))
            taskdb = tskdb_key.get()
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            uids=self.request.POST.getall('ckuser') # fetch all user
            if len(uids) > 0:
                for id in uids:
                    usd=ndb.Key('User',int(id)).get()
                    usd.taskassigned.append(taskname)
                    usd.put()
                    #keys.append(ndb.Key('User',int(id)))
                for task in taskdb.task:
                    if task.taskname == taskname:
                        task.assignstatus = 1
                taskdb.put()
                self.redirect('/taskboardDetails?key='+tskdbid)
            else:
                self.redirect('/taskboardDetails?key='+tskdbid)
        elif self.request.get('button') == 'Cancel':
            tskdbid=self.request.get("hdnid1").strip()
            self.redirect('/taskboardDetails?key='+tskdbid)
