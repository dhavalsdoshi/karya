from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from main_handler import MainHandler


application = webapp.WSGIApplication([('/', MainHandler)], debug=True)


def main():
  run_wsgi_app(application)
