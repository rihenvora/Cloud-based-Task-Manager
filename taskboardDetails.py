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


class taskboardDetails(webapp2.RequestHandler):
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
        tctoday=0
        tactive=0
        tcomplet=0
        totalt=0
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
                for task in lst.task:
                    if task.status=='Pending':
                        tactive+=1
                        totalt+=1
                    elif task.status=='Complete':
                        tcomplet+=1
                        totalt+=1
                    y=str(task.complete_date).strip(" ")
                    x=str(datetime.now()).strip(" ")
                    if str(y[0]) == str(x[0]):
                        tctoday+=1
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
        'showList':list,
        'listusr':listusr,
        'tskdb' : tskdb1,
        'tskdbid' : list1,
        'total' : totalt,
        'today' : tctoday,
        'active' : tactive,
        'complete' : tcomplet,
        }

        template = JINJA_ENVIRONMENT.get_template('taskboardDetails.html')
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
        list1=''
        keys=[]
        tskdbid=''
        # pull the current user from the request
        user = users.get_current_user()
        tskdbid=self.request.get("hdnid")
        if action == 'Insert':
            # determine if we have a user logged in or not

            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            tskdb_key = ndb.Key('TaskBoard',int(tskdbid))
            taskdb = tskdb_key.get()
            #list = EleVhe.query(EleVhe.email_address == user.email()).fetch()
            uids=self.request.POST.getall('ckusr') # fetch all user
            if len(uids) > 0:
                for id in uids:
                    usd=ndb.Key('User',int(id)).get()
                    usd.taskboard.append(tskdbid)
                    usd.put()
                    keys.append(ndb.Key('User',int(id)))
                    taskdb.user.append(ndb.Key('User',int(id)))
                    taskdb.put()

                self.redirect('/taskboardDetails?key='+tskdbid)
            else:
                self.redirect('/taskboardDetails?key='+tskdbid)
        elif self.request.get('button') == 'Cancel':
			self.redirect('/taskboardDetails?key='+tskdbid)
