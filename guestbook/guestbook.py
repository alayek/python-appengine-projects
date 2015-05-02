import webapp2
import cgi
from google.appengine.api import users

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
	"""docstring for MainPage"""
	def get(self):
		self.response.write(MAIN_PAGE_HTML)

class GuestBook(webapp2.RequestHandler):
	"""docstring for GuestBook"""
	def post(self):
		self.response.write("<html><body>You wrote:<pre>")
		self.response.write(cgi.escape(self.request.get('content')))
		self.response.write("</pre></body></html>")

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', GuestBook),
	], debug=True)
		
