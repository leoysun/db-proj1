
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

global_user_id = None # store user ID from the user ID input form in index.html

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

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

@app.route('/')
def showTables():
    global global_user_id
    # First, get the dining halls
    cursor = g.conn.execute(text("""
        SELECT DISTINCT dh.dhall_name, dh.address, dh.capacity, dh.hours
        FROM dining_halls dh
    """))
    dhalls = [dict(row) for row in cursor.mappings()]
    cursor.close()

    avg_rating_dict = {}
    # Then, get items for each dining hall by station
    for dhall in dhalls:
        avg_cursor = g.conn.execute(text(
           """
            SELECT AVG(e.rating)
            FROM evaluates e
            WHERE e.dhall_name=:dhall_name
           """
        ), {"dhall_name": dhall['dhall_name']})

        avg_rating = avg_cursor.fetchone()[0]
        avg_rating_dict[dhall['dhall_name']] = avg_rating

        # Fetch items for this specific dining hall, grouped by station
        items_cursor = g.conn.execute(text("""
            SELECT hi.dhall_name, hi.item_name, hi.dietary_info, hi.ingredients, hi.station, c.mealtime
            FROM contains c, has_item hi
            WHERE hi.dhall_name = c.dhall_name AND c.item_name = hi.item_name AND hi.dhall_name = :dhall_name
        """), {"dhall_name": dhall['dhall_name']})
        
        # Group items by station
        stations = {}
        for item in items_cursor.mappings():
            if item['station'] not in stations:
                stations[item['station']] = []
            stations[item['station']].append({
                'name': item['item_name'],
                'dietary_info': item['dietary_info'] or 'No info',
                'ingredients': item['ingredients'] or 'No info',
                'mealtime': item['mealtime']
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
        SELECT pr.*, e.dhall_name, d.item_name, e.mealtime, e.rating
        FROM discusses d, posts_reviews pr, evaluates e
        WHERE d.rid = e.rid AND e.rid = pr.rid
    """))
    reviews = reviews_cursor.mappings().all()
    reviews_cursor.close()

    context = {
        'data': dhalls
    }
    return render_template("index.html", global_user_id=global_user_id, avg_rating_dict=avg_rating_dict, **context)
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
#@app.route('/another')
#def another():
#  return render_template("another.html")

@app.route('/dhall_name', methods=['POST'])
def set_dhall_name():
  g.dhall_name = request.form.get('dhall_name')  # Retrieve the value of 'dhall_name' from the form
  print(g.dhall_name)
  return redirect('/')

@app.route('/reviews')
def showReviews():

  global global_user_id
  query = """
    SELECT pr.*, e.dhall_name, d.item_name, e.mealtime, e.rating
    FROM discusses d, posts_reviews pr, evaluates e
    WHERE d.rid = e.rid AND e.rid = pr.rid
    """
  
  cursor = g.conn.execute(text(query))
  g.conn.commit()
  reviews = cursor.mappings().all()
  cursor.close()
  context = dict(reviews=reviews)
  return render_template('reviews.html', global_user_id=global_user_id, **context)

@app.route('/submitUser', methods=['GET', 'POST'])
def submitUser():
  global global_user_id
  user_id = request.form.get('user_id')
  if not user_id:
    return "UNI cannot be blank", 400
  global_user_id = user_id

  # boolean
  is_admin = False
  username = request.form.get('username')
  password = request.form.get('password')

  admin_cursor = g.conn.execute(text("""
      SELECT user_id, password
      FROM Admin
      WHERE user_id = :user_id
      """), {'user_id': user_id})
  g.conn.commit()
  admins = admin_cursor.mappings().all()
  admin_cursor.close()

  if admins:
    admin_entry = admins[0]
    
    # Check if the user is an admin and password is incorrect
    if password == '' or password != admin_entry['password']:
        return "Wrong password", 400
  else:
    return "Not an admin", 400
  
  user_params = {
      'user_id': request.form['user_id'],
      'username': request.form['username'],
    }
  g.conn.execute(text("""
      INSERT INTO Users (user_id, username)
      VALUES (:user_id, :username)
      ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username
      """), user_params)
  g.conn.commit()
  return redirect('/')

@app.route('/deleteReviews', methods=['GET', 'POST'])
def deleteReviews():
   # display the reviews eligible for deletion based on user ID
   global global_user_id
   if not global_user_id:
      return "Make sure you have submitted your UNI on the home page", 400
   query = """
    SELECT pr.*, e.dhall_name, d.item_name, e.mealtime, e.rating
    FROM discusses d, posts_reviews pr, evaluates e
    WHERE d.rid = e.rid AND e.rid = pr.rid AND pr.user_id = :user_id
    """
   cursor = g.conn.execute(text(query), {'user_id': global_user_id})
   g.conn.commit()
   reviews = cursor.mappings().all()
   cursor.close()
   context = dict(reviews=reviews)
   return render_template('deleteReviews.html', global_user_id=global_user_id, **context) 

@app.route('/submitReview', methods=['GET', 'POST'])
def submitReview():
    user_id = request.form.get('user_id')  # Get user ID from form input
    dhall_name = request.form.get('dhall_name')
    rating = request.form.get('rating')
    description = request.form.get('description')
    item_name = request.form.get('item_name')

    # Ensure user_id is not empty
    if not user_id:
        return "UNI is required to submit a review.", 400
        
    rid = str(uuid.uuid4())[:20]
    current_time = datetime.now()
    
    # Insert the review and rating
    try:
        # Insert into Menu_is_from
        menu_is_from_params = {
            'dhall_name': request.form['dhall_name'],
            'mealtime': request.form['mealtime'],
            'date': current_time.date()
        }
        g.conn.execute(text("""
            INSERT INTO Menu_is_from (dhall_name, mealtime, date)
            VALUES (:dhall_name, :mealtime, :date)
            ON CONFLICT (dhall_name, mealtime) DO UPDATE SET date = EXCLUDED.date
        """), menu_is_from_params)
        g.conn.commit()

        # Insert into Posts_Reviews
        review_params = {
            'user_id': request.form['user_id'],
            'datetime': current_time,
            'rid': rid,
            'description': request.form['description'],
        }
        g.conn.execute(text("""
            INSERT INTO Posts_Reviews (user_id, datetime, rid, description)
            VALUES (:user_id, :datetime, :rid, :description) 
        """), review_params)
        g.conn.commit()
        
        # Insert into evaluates
        evaluates_params = {
            'dhall_name': request.form['dhall_name'],
            'mealtime': request.form['mealtime'],
            'rid': rid,
            'rating': request.form['rating']
        }
        g.conn.execute(text("""
            INSERT INTO evaluates (dhall_name, mealtime, rid, rating)
            VALUES (:dhall_name, :mealtime, :rid, :rating)
        """), evaluates_params)
        g.conn.commit()
        
        # Insert into Discusses
        discusses_params = {
            'rid': rid,
            'item_name': request.form['item_name'],
            'dhall_name': request.form['dhall_name'],
            'rating': request.form['rating']
        }
        g.conn.execute(text("""
            INSERT INTO Discusses (rid, item_name, dhall_name, rating)
            VALUES (:rid, :item_name, :dhall_name, :rating)
        """), discusses_params)
        g.conn.commit()

        # Insert into Judges
        #judges_params = {
        #    'rating': request.form['rating'],
        #    'user_id': request.form['user_id'],
        #    'dhall_name': request.form['dhall_name'],
        #    'mealtime': request.form['mealtime'],
        #}
        #g.conn.execute(text("""
        #    INSERT INTO Judges (rating, user_id, dhall_name, mealtime)
        #    VALUES (:rating, :user_id, :dhall_name, :mealtime)
        #"""), judges_params)
        #g.conn.commit()

        # Insert into rates
        #rating_params = {
        #    'user_id': request.form['user_id'],
        #    'dhall_name': request.form['dhall_name'],
        #    'rating': request.form['rating']
        #}
        #g.conn.execute(text("""
        #    INSERT INTO rates (rating, user_id, dhall_name)
        #    VALUES (:rating, :user_id, :dhall_name)
        #    ON CONFLICT (user_id, dhall_name) 
        #   DO UPDATE SET rating = EXCLUDED.rating
        #"""), rating_params)
        #g.conn.commit()

        return redirect('/reviews')
        
    except Exception as e:
        print(f"Error submitting review: {e}")
        g.conn.rollback()
        return f"Error submitting review: {e}", 500

@app.route('/deleteSingleReview', methods=['POST'])
def deleteSingleReview():
  global global_user_id
  if not global_user_id:
      return "Something went wrong with signing in, please input your UNI on the homepage again", 400
   
  rid = request.form.get('rid')
  print(f"Received rid: {rid}")
  if not rid:
    return "Error with selecting review", 400
  
  try:
    # delete from rates
    #g.conn.execute(text("""
    #    DELETE FROM rates
    #    WHERE rid IN (
    #     SELECT rid 
    #        FROM posts_reviews 
    #        WHERE rid = :rid AND user_id = :user_id )
    #    """), {"rid": rid, "user_id": global_user_id}
    #)
    #g.conn.commit()

    # delete from judges
    #g.conn.execute(text("""
    #    DELETE FROM judges
    #    WHERE rid IN (
    #      SELECT rid 
    #        FROM evaluates 
    #        WHERE rid = :rid AND user_id = :user_id )
    #    """), {"rid": rid, "user_id": global_user_id}
    #)
    #g.conn.commit()

    # delete from discusses
    g.conn.execute(text("""
        DELETE FROM discusses 
        WHERE rid = :rid;
        """), {"rid": rid})
    g.conn.commit()
    
    # delete from evaluates
    g.conn.execute(text("""
        DELETE FROM evaluates 
        WHERE rid = :rid;
        """), {"rid": rid})
    g.conn.commit()

    # delete from posts_reviews
    g.conn.execute(text("""
        DELETE FROM Posts_Reviews 
        WHERE rid = :rid AND user_id = :user_id;
        """), {"rid": rid, "user_id": global_user_id})
    g.conn.commit()

    return redirect('/deleteReviews')

  except Exception as e:
        g.conn.rollback()
        print(f"Error deleting review: {e}")
        return f"Error deleting review: {e}", 500


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