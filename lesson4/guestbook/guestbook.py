import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)

        # Ancestor Queries, as shown here, are strongly consistent
        # with the High Replication Datastore. Queries that span
        # entity groups are eventually consistent. If we omitted the
        # ancestor from this query there would be a slight chance that
        # Greeting that had just been written would not show up in a
        # query.
        # [START query]
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(Greeting.date)

        greetings = greetings_query.fetch(10)
        # [END query]

        user = users.get_current_user()
        for greeting in greetings:
            if greeting.author:
                author = greeting.author.email
                if user and user.user_id() == greeting.author.identity:
                    author += ' (You)'
                self.response.write('<b>%s</b> wrote:' % author)
            else:
                self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote>%s</blockquote>' %
                                cgi.escape(greeting.content))
            # Use POST to edit & delete entry
            self.response.write("""
                                <div style="display: flex;">
                                <form action="edit" method="post">
                                <input type="hidden" name="key" value="%s">
                                <input type="submit" value="Edit">
                                </form>
                                <form action='delete' method='post'>
                                <input type="hidden" name="key" value="%s">
                                <input type="hidden" name="guestbook_name" value="%s">
                                <input type="submit" value="Delete">
                                </form>
                                </div>
                                <hr color="#CFD8DC">
                                """ % (greeting.key.urlsafe(), greeting.key.urlsafe(), guestbook_name))

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'guestbook_name':
                                              guestbook_name})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
                            (sign_query_params, cgi.escape(guestbook_name),
                             url, url_linktext))
    def post(self):
        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(Greeting.date)
        greetings = greetings_query.fetch()
        key = self.request.get("key")
        
        user = users.get_current_user()
        for greeting in greetings:
            if greeting.key.urlsafe() == key:
                self.response.write("""
                                    <form action="/sign?%s" method="post">
                                    <div><textarea name="content" rows="3" cols="60">%s</textarea></div>
                                    <input type="submit" value="Finish">
                                    <input type="hidden" name="edit" value="1">
                                    <input type="hidden" name="key" value="%s">
                                    </form>
                                    <form action="/" method="get">
                                    <input type="hidden" name="guestbook_name" value="%s">
                                    <input type="submit" value="Cancel">
                                    </form>
                                    """ % (urllib.urlencode({"guestbook_name": guestbook_name}), greeting.content,
                                        key, guestbook_name))

# [END main_page]

# [START guestbook]
class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        edit = self.request.get("edit")
        
        greeting = None
        if bool(edit):
            greeting = ndb.Key(urlsafe=self.request.get("key")).get()
        else:
            greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

# Delete post handler
class Delete(webapp2.RequestHandler):
    def post(self):
        key = ndb.Key(urlsafe=self.request.get("key"))
        key.delete()
        self.redirect("/?"+ urllib.urlencode({"guestbook_name": self.request.get("guestbook_name")}))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/edit', MainPage),
    ('/sign', Guestbook),
    ('/delete', Delete),
], debug=True)
