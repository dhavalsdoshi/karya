import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from apiclient.discovery import build
import httplib2
from oauth2client.appengine import OAuth2Decorator
import settings
from django.utils import simplejson

decorator = OAuth2Decorator(client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET,
                            scope=settings.SCOPE,
                            user_agent='karya')

class Task(object):
    def __init__(self, task_dict):
        self.name = task_dict['title']
        self.is_done = True if task_dict['status'] == 'completed' else False
        
    def __dict__(self):
        return {'name':self.name, 'isDone': self.is_done}
        
class MainHandler(webapp.RequestHandler):

    @decorator.oauth_required
    def get(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            result = service.tasks().list(tasklist='@default').execute()
            tasks = result.get('items',[])
            logging.info(tasks)
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, {'tasks':tasks}))
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
                                    
