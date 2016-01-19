# Lession 4.6: What is Your Birthday

# This lesson will involve us validating a user's birthday. Input validation is crucial
# in order to make sure data entered from the user can be processed without errors.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4175328805/e-48754024/m-48714316


import webapp2
import cgi

form = """
<form method="post">
    What is your birthday?
    <br>
    <label> Month
        <input type="text" name="month" value=%(month)s style="color: %(valid_month)s">
    </label>

    <label> Day
        <input type="text" name="day" value=%(day)s style="color: %(valid_day)s">
    </label>

    <label> Year
        <input type="text" name="year" value=%(year)s style="color: %(valid_year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

def escape_html(s):
    if s == "":
        return "''"
    return cgi.escape(s, quote = True)

def valid_color(valid):
    if valid:
        return "black"
    else:
        return "red"

def valid_month(month, months=["January", "February", "March", "April", 
    "May", "June", "July", "August", "September", "October", "November", "December"]):
    if month:
        month_dic = dict((m[:3].lower(), m) for m in months)
        key = month[:3].lower()
        if key in month_dic:
            return month_dic[key]

def valid_day(day):
    if day.isdigit():
        d = int(day)
        if d > 0 and d < 32:
            return int(day)

def valid_year(year):
    if year.isdigit():
        y = int(year)
        if y > 1900 and y < 2020:
            return year

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", valid_month=True, day="", valid_day=True, year="", valid_year=True):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "valid_month": valid_color(valid_month),
                                        "day": escape_html(day),
                                        "valid_day": valid_color(valid_day),
                                        "year": escape_html(year),
                                        "valid_year": valid_color(valid_year)})
    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend",
                                  user_month, month, user_day, day, user_year, year)
        else:
            self.redirect("/thanks")
            

        ''' This is the Udacity version
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend",
                                  user_month, user_day, user_year)
        else:
            self.response.out.write("Thanks! That's a totally valid day!")
        '''

        ''' This version deletes all invalid text from the text box
        user_month = valid_month(self.request.get("month"))
        user_day = valid_day(self.request.get("day"))
        user_year = valid_year(self.request.get("year"))

        if user_month and user_day and user_year:
            self.response.out.write_form("Thanks! That's a totally valid day!")
        else:
            self.write_form("That doesn't look valid to me.", user_month, user_day, user_year)
        '''

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([("/", MainPage), ("/thanks", ThanksHandler)], debug = True)