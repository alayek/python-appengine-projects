import webapp2
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
	"""docstring for MainPage"""
	def get(self):
		# check for active Google account session
		user = users.get_current_user()

		if user:
			# logged in user
			self.response.headers['Content-Type'] = 'text/plain';
			self.response.write("Hello, %s" % user.nickname())
		else:
			# not logged in
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
	], 	debug=True)