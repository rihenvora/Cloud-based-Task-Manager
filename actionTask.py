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


class actionTask(webapp2.RequestHandler):
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
        utask=[]
        ut=''
        user = users.get_current_user()
        #list1=self.request.get('key').strip("Key()").split(",")
        list1=int(self.request.get('key'))
        taskname=self.request.get('key1').strip()
        actionperform =self.request.get('key2')

        if actionperform == 'complete':
            tskdb_key = ndb.Key('TaskBoard',int(list1))
            taskdb = tskdb_key.get()
            for task in taskdb.task:
                if task.taskname == taskname:
                    task.status = 'Complete'
                    task.complete_date = datetime.now()
            taskdb.put()
            self.redirect('/taskboardDetails?key='+str(list1))

        elif actionperform == 'delete':
            tskdb_key = ndb.Key('TaskBoard',int(list1))
            taskdb = tskdb_key.get()
            for task in taskdb.task:
                if task.taskname != taskname:
                    taskd.append(task)
            for user in taskdb.user:
                #user_key = ndb.Key('User',int(user))
                userd = user.get()
                for ut in userd.taskassigned:
                    if ut == taskname:
                        ut1 = userd.key.get()
                        for ut2 in ut1.taskassigned:
                            if ut2 != taskname:
                                utask.append(ut2)
                        ut1.taskassigned=utask
                        ut1.put()
            taskdb.task=taskd
            taskdb.put()
            self.redirect('/taskboardDetails?key='+str(list1))
        elif actionperform == 'edit':
            list=[]
            listr=''
            if user:
                #Task Board
                tskdb_key = ndb.Key('TaskBoard',list1)
                taskdb = tskdb_key.get()

                list.append(taskdb)
                for lst in list:
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
            'task' : taskd,
            'taskboard' : list,
            'tskbdid' : list1,
            'taskname' : taskname
            }

            template = JINJA_ENVIRONMENT.get_template('actionTask.html')
            self.response.write(template.render(template_values))
    #-----------------------------------------------------------------
    def post(self):
        self.response.headers['Content-Type']='text/html'
        action = self.request.get('button')
        # pull the current user from the request
        user = users.get_current_user()
        if action == 'Edit':
            # determine if we have a user logged in or not
            tskdbid=self.request.get("hdnid").strip()
            taskname=self.request.get("hdntaskname").strip()
            tskdb_key = ndb.Key('TaskBoard',int(tskdbid))
            taskdb = tskdb_key.get()

            tasknamel=[]
            for task in taskdb.task:
                tasknamel.append(task.taskname)

            if self.request.get("name") not in  tasknamel:
                for task in taskdb.task:
                    #print(task)
                    if task.taskname == taskname:
                        task.taskname = self.request.get("name")
                        task.due_date = datetime.strptime(self.request.get("date"), '%Y-%m-%d')
                taskdb.put()

                for user in taskdb.user:
                    userd = user.get()
                    for ut in userd.taskassigned:
                        if ut == taskname:
                            ut1 = userd.key.get()
                            for ut2 in ut1.taskassigned:
                                if ut2 == taskname:
                                    ut1.taskassigned=[self.request.get("name")]
                                #ut1.taskassigned=utask
                                ut1.put()

            self.redirect('/taskboardDetails?key='+str(tskdbid))
        elif self.request.get('button') == 'Cancel':
            tskdbid=self.request.get("hdnid").strip()
            self.redirect('/taskboardDetails?key='+tskdbid)
