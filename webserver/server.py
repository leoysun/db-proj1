
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort
from datetime import datetime
import uuid

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://jld2251:juliaduckey@104.196.222.236/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# The string needs to be wrapped around text()

#conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);"""))
#conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))

# To make the queries run, we need to add this commit line
#conn.commit() 

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
# @app.route('/')
"""
def showTables():
  cursor = g.conn.execute(text("""
                               # SELECT dh.dhall_name, dh.address, dh.capacity, dh.hours, hi.item_name, hi.dietary_info, hi.ingredients
                               # FROM dining_halls dh INNER JOIN has_item hi
                               # ON dh.dhall_name = hi.dhall_name
                               # """))
  #### Access in dhalls.html using dhalls['item_name'], dhalls['dietary_info'], dhalls['ingredients'], etc. Maybe use AI for frontend fitting info in
  #### NOTE: above query is still flawed as it doesn't include the dates and mealtime that the items are presented during. 
  #### This is in the table "Menu_is_from" I believe. But that requires another join which we can figure out later if we want.
"""
  g.conn.commit()
  dhalls = []
  results = cursor.mappings().all()
  for result in results:
    dhalls.append(result)
  cursor.close()

  context = dict(data=dhalls)
  return render_template("index.html", **context)
  """
@app.route('/')
def showTables():
    # First, get the dining halls
    cursor = g.conn.execute(text("""
        SELECT DISTINCT dh.dhall_name, dh.address, dh.capacity, dh.hours
        FROM dining_halls dh
    """))
    dhalls = [dict(row) for row in cursor.mappings()]
    cursor.close()

    # Then, get items for each dining hall by station
    for dhall in dhalls:
        # Fetch items for this specific dining hall, grouped by station
        items_cursor = g.conn.execute(text("""
            SELECT hi.dhall_name, hi.item_name, hi.dietary_info, hi.ingredients, hi.station, c.mealtime
            FROM contains c, has_item hi
            WHERE hi.dhall_name = c.dhall_name AND c.item_name = hi.item_name AND hi.dhall_name = :dhall_name
        """), {"dhall_name": dhall['dhall_name']})
        #### ENSURE THIS QUERY WORKS
        
        # Group items by station
        stations = {}
        for item in items_cursor.mappings():
            if item['station'] not in stations:
                stations[item['station']] = []
            stations[item['station']].append({
                'name': item['item_name'],
                'dietary_info': item['dietary_info'] or 'No info'
            })
        
        dhall['stations'] = [
            {
                'station': station, 
                'items': items
            } for station, items in stations.items()
        ]
        items_cursor.close()


    # Fetch reviews
    reviews_cursor = g.conn.execute(text("""
        SELECT DISTINCT pr.*, j.rating, e.dhall_name
        FROM posts_reviews pr 
        INNER JOIN evaluates e ON pr.rid = e.rid
        INNER JOIN judges j ON j.user_id = pr.user_id AND j.dhall_name = e.dhall_name AND j.mealtime = e.mealtime
        ORDER BY pr.datetime DESC
        LIMIT 5
    """))
    reviews = reviews_cursor.mappings().all()
    reviews_cursor.close()

    context = {
        'data': dhalls
    }
    return render_template("index.html", **context)
# @app.route('/')
# def index():
"""
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
#  print(request.args)

  #
  # example of a database query 
  #
  #cursor = g.conn.execute(text("SELECT name FROM test"))
  #g.conn.commit()

  # 2 ways to get results

  # Method 1 - Indexing result by column number
  #names = []
  #for result in cursor:
  #  names.append(result[0])  

  # Method 2 - Indexing result by column name
  #names = []
  #results = cursor.mappings().all() 
  #for result in results:
  #  names.append(result["name"])

  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  
  #context = dict(data = names)
  
  #<div>{{data}}</div>
  
       # creates a <div> tag for each element in data
       # will print:
       #
       #   <div>grace hopper</div>
       #   <div>alan turing</div>
       #   <div>ada lovelace</div>
       #
  #{% for n in data %}
  #    <div>{{n}}</div>
  #{% endfor %}
  
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  # return render_template("index.html") #, **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")

# Example of adding new data to the database
@app.route('/add', methods=['ADD','POST'])
def add(): 
  rating = request.form['rating']
  params_dict = {"rating":rating, "user_id":g.user_id, "dhall_name":g.dhall_name} # ADD FORMS TO ADJUST THE DHALLNAME AND USERID
  g.conn.execute(text("""INSERT INTO rates(rating, user_id, dhall_name) 
                      VALUES (:rating, :user_id, :dhall_name)
                      ON CONFLICT (user_id, dhall_name) DO UPDATE SET rating = EXCLUDED.rating")"""), params_dict)
  g.conn.commit()

  return redirect('/')

@app.route('/id', methods=['POST'])
def set_userid():
  try:
    g.user_id = request.form.get('user_id')  # Retrieve the value of 'user_id' from the form
    g.conn.execute(text('INSERT INTO users(user_id) VALUES (:user_id)'), {'user_id': g.user_id})
    g.conn.commit()
  except Exception as e:
    
    redirect('/')
    Response("Your User ID is already in use.") # NOTE: THIS IS NOT WORKING. BUT IT'S OKAY FOR NOW
  return redirect('/')

@app.route('/dhall_name', methods=['POST'])
def set_dhall_name():
  g.dhall_name = request.form.get('dhall_name')  # Retrieve the value of 'dhall_name' from the form
  print(g.dhall_name)
  return redirect('/')

@app.route('/rate', methods=['POST'])
def set_rating():
  g.rating = request.form.get('rating')  # Retrieve the value of 'rating' from the form
  print(g.rating)
  return redirect('/add')

#currently in progress
#@app.route('/search')
#def search():
#  g.search = request.form.get('search') # MAKE THIS MORE IN DEPTH. WANT TO SEARCH FOR WHATEVER THE SEARCH FORM GIVES. FROM ALL DHALL INFO.
#  cursor = g.conn.execute(text("SELECT"))
#  return render_template("search.html, ")

#TODO: get all food info on dhall page
@app.route('/reviews')
def showReviews():
  #cursor = g.conn.execute(text("""
  #  SELECT dhall_name 
  #  FROM dining_halls dh, evaluates e
  #  WHERE dh.dhall_name = e.dhall_name
  #  """))
  #g.conn.commit()
  #dhalls = [row[0] for row in cursor]
  #cursor.close()
    
  # Get SOME reviews with dining hall info
  query = """
    SELECT DISTINCT pr.*, j.rating, e.dhall_name
    FROM posts_reviews pr INNER JOIN evaluates e
    ON pr.rid = e.rid
    INNER JOIN judges j
    ON j.user_id = pr.user_id AND j.dhall_name = e.dhall_name AND j.mealtime = e.mealtime
    """
  
  cursor = g.conn.execute(text(query))
  g.conn.commit()
  reviews = cursor.mappings().all()
  cursor.close()
  context = dict(reviews=reviews)
  return render_template('reviews.html', **context)

@app.route('/submitUser', methods=['GET', 'POST'])
def submitUser():
  user_id = request.form.get('user_id')
  if not user_id:
    return "User ID cannot be blank", 400
   
  user_params = {
      'user_id': request.form['user_id'],
      'username': request.form['username'],
    }
  g.conn.execute(text("""
      INSERT INTO Users (user_id, username)
      VALUES (:user_id, :username)
      """), user_params)
  g.conn.commit()
  return redirect('/')
  

@app.route('/submitReview', methods=['GET', 'POST'])
def submitReview():
    dhall_name = request.form.get('dhall_name')
    rating = request.form.get('rating')
    description = request.form.get('description')
    user_id = request.form.get('user_id')  # Get user ID from form input

    # Ensure user_id is not empty
    if not user_id:
        return "User ID is required to submit a review.", 400
        
    rid = str(uuid.uuid4())[:20]
    current_time = datetime.now()
    
    # Insert the review and rating
    try:
        # Insert into Posts_Reviews
        review_params = {
            'user_id': request.form['user_id'],
            'datetime': current_time,
            'rid': rid,
            'description': request.form['description']
        }
        g.conn.execute(text("""
            INSERT INTO Posts_Reviews (user_id, datetime, rid, description)
            VALUES (:user_id, :datetime, :rid, :description)
        """), review_params)
        
        # Insert into rates
        rating_params = {
            'user_id': request.form['user_id'],
            'dhall_name': request.form['dhall_name'],
            'rating': request.form['rating']
        }
        g.conn.execute(text("""
            INSERT INTO rates (rating, user_id, dhall_name)
            VALUES (:rating, :user_id, :dhall_name)
            ON CONFLICT (user_id, dhall_name) 
            DO UPDATE SET rating = EXCLUDED.rating
        """), rating_params)

        # Insert into Menu_is_from
        menu_is_from_params = {
            'dhall_name': request.form['dhall_name'],
            'mealtime': request.form['mealtime'],
            'date': current_time.date()
        }
        g.conn.execute(text("""
            INSERT INTO Menu_is_from (dhall_name, mealtime, date)
            VALUES (:dhall_name, :mealtime, :date)
        """), menu_is_from_params)
        g.conn.commit()
        
        # Insert into evaluates
        evaluates_params = {
            'dhall_name': request.form['dhall_name'],
            'mealtime': request.form['mealtime'],
            'rid': rid
        }
        g.conn.execute(text("""
            INSERT INTO evaluates (dhall_name, mealtime, rid)
            VALUES (:dhall_name, :mealtime, :rid)
        """), evaluates_params)
        g.conn.commit()

        return redirect('/reviews')
        
    except Exception as e:
        print(f"Error submitting review: {e}")
        g.conn.rollback()
        return f"Error submitting review: {e}", 500

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    
  app.run(debug=True)

