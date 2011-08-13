from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from apiclient.discovery import build
import httplib2
from oauth2client.appengine import OAuth2Decorator
import settings

decorator = OAuth2Decorator(client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET,
                            scope=settings.SCOPE,
                            user_agent='mytasks')


class MainHandler(webapp.RequestHandler):

   @decorator.oauth_required
   def get(self):
     service = build('tasks', 'v1', http=decorator.http())
     tasks = service.tasks().list(tasklist='@default').execute()
     self.response.out.write('<html><body><ul>')
     for task in tasks['items']:
       self.response.out.write('<li>%s</li>' % task['title'])
     self.response.out.write('</ul></body><html>')

application = webapp.WSGIApplication([('/', MainHandler)], debug=True)


def main():
  run_wsgi_app(application)