import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JIJNA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions = ['jinja2.ext.autoescape'],autoescape=True,)

#
# DB Schema, with two tables
#
class Author(ndb.Model):
	"""submodel for representing an Author"""
	identity = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
	"""A main Model for representing a post"""
	author = ndb.StructuredProperty(Author)	
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	return ndb.Key('Guestbook', guestbook_name)


class MainPage(webapp2.RequestHandler):
	"""RequestHandler for main page"""
	def get(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

		# get greetings in reverse chronological order
		greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10) # fetch only 10 for now

		user = users.get_current_user()

		# if user is logged in, give logout option
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		# prepare template values
		template_values = {
			'user' : user,
			'greetings' : greetings,
			'guestbook_name' : urllib.quote_plus(guestbook_name),
			'url' : url,
			'url_linktext' : url_linktext,
		}

		template = JIJNA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

# handle the post submission here
class GuestBook(webapp2.RequestHandler):
	"""docstring for GuestBook"""
	def post(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = Author(
				identity = users.get_current_user().user_id(),
				email = users.get_current_user().email())

		greeting.content = self.request.get('content')
		greeting.put() ## put in the DB

		query_params = {'guestbook_name' : guestbook_name}
		self.redirect('/?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', GuestBook),
	], debug = True)
