import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
import settings
from django.utils import simplejson

decorator = OAuth2Decorator(client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET,
                            scope=settings.SCOPE,
                            user_agent='karya')

class Task(object):
    def __init__(self, task_dict):
        self.title = task_dict['title']
        self.is_done = True if task_dict['status'] == 'completed' else False

    def __dict__(self):
        return {'title': self.title, 'isDone': self.is_done}

class TaskList(object):
    def __init__(self, task_list_dict, tasks):
        self.title = task_list_dict['title']
        self.id= task_list_dict['id']
        self.tasks = tasks

    def __dict__(self):
        return {'title': self.title, 'id': self.id, 'tasks': [t.__dict__() for t in self.tasks]}


class MainHandler(webapp.RequestHandler):
    @decorator.oauth_required
    def get(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            tasklistsResult = service.tasklists().list().execute()
            logging.info(tasklistsResult.get('items', []))
            result = service.tasks().list(tasklist='@default').execute()
            tasks = result.get('items', [])
            logging.info(tasks)
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, {'tasks': tasks}))
        else:
            url = decorator.authorize_url()
            logging.info(url)
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, {'url': url}))


class TasksHandler(webapp.RequestHandler):
    @decorator.oauth_required
    def get(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            result = service.tasks().list(tasklist='@default').execute()
            tasks = result.get('items',[])
            tasks = [Task(t) for t in tasks]
            self.response.out.write(simplejson.dumps([t.__dict__() for t in tasks]))

    def remove(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            result = service.tasks().list(tasklist='@default').execute()
            tasks = result.get('items',[])
            tasks = [Task(t) for t in tasks]
            self.response.out.write(simplejson.dumps([t.__dict__() for t in tasks]))

class TaskListsHandler(webapp.RequestHandler):
    @decorator.oauth_required
    def get(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            task_lists_result = service.tasklists().list().execute()
            task_lists = []
            logging.info(task_lists_result['items'])
            for task_list in task_lists_result['items']:
                task_list_id = task_list.get('id','@default')
                task_list_title = task_list['title']
                logging.info(task_list_id)
                logging.info(task_list_title)
                result = service.tasks().list(tasklist=task_list_id).execute()
                tasks = result.get('items', [])
                tasks = [Task(t) for t in tasks]
                task_lists.append(TaskList(task_list,tasks))
            self.response.out.write(simplejson.dumps([t.__dict__() for t in task_lists]))

#    def delete(self, *args):
#        if decorator.has_credentials():
#            taskListId = "get from args"
#            service = build('tasks', 'v1', http=decorator.http())
#            service.tasklists().delete(tasklist=taskListId).execute()
#
#    def put(self, *args):
#        if decorator.has_credentials():
#            service = build('tasks', 'v1', http=decorator.http())
#            taskList = service.tasklists().get(tasklist='taskListID').execute()
#            taskListNewTitle = "get from args"
#            taskList['title'] = taskListNewTitle
#            result = service.tasklists().update(tasklist=taskList['id'], body=taskList).execute()
#            print result['title']
#
#    def post(self, *args):
#        if decorator.has_credentials():
#            service = build('tasks', 'v1', http=decorator.http())
#            taskListTitle = "get from args"
#            taskList = {
#                'title': taskListTitle
#            }
#            result = service.tasklists().insert(body=taskList).execute()
#            print result['id']