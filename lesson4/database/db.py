from collections import namedtuple
import sqlite3

Weather = namedtuple("Weather", ["main", "description", "temp", "temp_hi", "temp_lo"])
weather_list = [Weather("clouds", "overcast clouds", 289.5, 292.04, 287.04),
                Weather("clouds", "broken clouds", 293.25, 295.37, 289.82),
                Weather("mist", "mist", 283.73, 285.15, 282.15)]

# SQL: Creating a new table
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE weather (main text, description text, temp float, temp_hi float, temp_lo float)")

# SQL: Inserting new values
for w in weather_list:
    db.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?)", w)


def row_by_temp_ascending():
    c = db.execute("SELECT * FROM weather ORDER BY temp ASC")   # DESC = descending order
    return c.fetchall()

def temp_descending():
    cursor = db.execute("SELECT temp FROM weather ORDER BY temp DESC")
    return [tup[0] for tup in cursor]

# SQL: Creating an index (hashtable)
def create_index(key):
    db.execute("CREATE INDEX weather_index ON weather("+key+")")