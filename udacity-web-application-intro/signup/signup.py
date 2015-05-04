import re
import cgi
import webapp2

def validate(username, password, verify_password, email):
	msg = {}

	username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	password_regex = re.compile(r"^.{3,20}$")
	email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

	if not username_regex.match(username):
		msg['username'] = 'That\'s not a valid username.'
	if not password_regex.match(password):
		msg['password'] = 'That wasn\'t a valid password.'
		return msg

	if password != verify_password:
		msg['verify_password'] = 'Your passwords didn\'t match.'
		return msg

	if email and not email_regex.match(email):
		msg['email'] = 'That\'s not a valid email.'
		return msg

	return msg

class SignUpPage(webapp2.RequestHandler):
	"""SignUp request handler"""
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<html><body>')
		self.response.write('<form method="POST">')
		self.response.write('<label>Username<input type="text" name="username"></label></br></br>')
		self.response.write('<label>Password<input type="password" name="password"></label></br></br>')
		self.response.write('<label>Verify Password<input type="password" name="verify"></label></br></br>')
		self.response.write('<label>Email<input type="text" name="email"></label></br></br>')
		self.response.write('</br></br><input type="submit" value="Sign Up"></form></body></html>')

	def post(self):
		username = self.request.get('username')
		email = self.request.get('email')
		password = self.request.get('password')
		verify = self.request.get('verify')

		failure = validate(cgi.escape(username), cgi.escape(password), cgi.escape(verify), cgi.escape(email))

		if failure:
			self.response.headers['Content-Type'] = 'text/html'
			self.response.write('<html><body>')
			self.response.write('<form method="POST">')
			if 'username' in failure:
				self.response.write('<label>Username<input type="text" value="%s" name="username">%s</label></br></br>' % (cgi.escape(username), failure['username']))
			else:
				self.response.write('<label>Username<input type="text" value="%s" name="username"></label></br></br>' % cgi.escape(username))
			if 'password' in failure:
				self.response.write('<label>Password<input type="password" name="password">%s</label></br></br>' % failure['password'])
			else:
				self.response.write('<label>Password<input type="password" name="password"></label></br></br>')
			if 'verify_password' in failure:
				self.response.write('<label>Verify Password<input type="password" name="verify">%s</label></br></br>' % failure['verify_password'])
			else:
				self.response.write('<label>Verify Password<input type="password" name="verify"></label></br></br>')
			if 'email' in failure:
				self.response.write('<label>Email<input type="text" value="%s" name="email">%s</label></br></br>' % (cgi.escape(email), failure['email']))
			else:
				self.response.write('<label>Email<input type="text" value="%s" name="email"></label></br></br>' % cgi.escape(email))
			self.response.write('</br></br><input type="submit" value="Sign Up"></form></body></html>')
			return
		else:
			self.redirect('/welcome?username=%s' % cgi.escape(username))	
			return

class Welcome(webapp2.RequestHandler):
	"""docstring for Welcome"""
	def get(self):
		username = cgi.escape(self.request.get('username'))
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("<html><body><h1>Welcome, %s</h1></body></html>" % username)

app = webapp2.WSGIApplication([
	('/signup', SignUpPage),
	('/welcome', Welcome),
	], 	debug=True)
		

		
