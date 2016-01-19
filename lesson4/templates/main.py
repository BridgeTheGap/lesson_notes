# Lession 4.7: Writing a Basic Form

# We'll start off writing a basic form in HTML using multiline strings to understand how
# we can process and substitute our variables into the HTML string we created.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4186408748/e-662529352/m-684819008

import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        food_list = self.request.get_all("food")
        self.render("shopping_list.html", food_list=food_list)

class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get("n")
        if n.isdigit():
            n = int(n)
            self.render("fizzbuzz.html", n = n)
        else:
            self.redirect("invalid")

class InvalidHandler(Handler):
    def get(self):
        self.response.out.write("Invalid operation. Input a valid fizzbuzz number.")

app = webapp2.WSGIApplication([("/", MainPage),
                               ("/fizzbuzz", FizzBuzzHandler),
                               ("/invalid", InvalidHandler),
                              ],
                              debug=True)
