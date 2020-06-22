from google.appengine.ext import ndb


class Task(ndb.Model):
    taskname = ndb.StringProperty()
    created_by = ndb.StringProperty()
    taskboardid = ndb.StringProperty()
    due_date = ndb.DateTimeProperty()
    status=ndb.StringProperty(default="Pending")
    assignstatus = ndb.IntegerProperty(default=0)
    complete_date=ndb.DateTimeProperty()
    created_date=ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    email_address = ndb.StringProperty()
    name = ndb.StringProperty()
    taskboard = ndb.StringProperty(repeated=True)
    taskassigned = ndb.StringProperty(repeated=True)

class TaskBoard(ndb.Model):
    #task_id = ndb.IntegerProperty()
    user_id = ndb.IntegerProperty()
    created_by=ndb.StringProperty()
    taskids=ndb.StringProperty(repeated=True)
    taskboardname=ndb.StringProperty()
    user = ndb.KeyProperty(kind='User', repeated=True)
    task = ndb.StructuredProperty(Task, repeated=True)
