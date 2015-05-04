import webapp2
import cgi

def rot13(string):
	new_string = ''
	for char in string:
		temp = char
		if char.isalpha():
			if char.islower():
				temp = chr(((ord(char) + 13 - ord('a')) % 26) + ord('a'))
			else:
				temp = chr(((ord(char) + 13 - ord('A')) % 26) + ord('A'))
		new_string += temp
	return new_string

class MainPage(webapp2.RequestHandler):
	"""MainPage will handle requests"""
	def get(self):
		# send the html response
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("<html><body>")

		self.response.write("<form method='POST'>")
		self.response.write("<textarea name='text' rows='10' cols='60'></textarea></br>")
		self.response.write("<input type='submit' value='submit'>")
		self.response.write("</form></body></html>")

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("<html><body>")

		self.response.write("<form method='POST'>")
		self.response.write("<textarea name='text' rows='10' cols='60'>%s</textarea></br>" % cgi.escape(rot13(self.request.get('text'))))
		self.response.write("<input type='submit' value='submit'>")
		self.response.write("</form></body></html>")

app = webapp2.WSGIApplication([
	('/', MainPage),
	], 	debug=True)
		