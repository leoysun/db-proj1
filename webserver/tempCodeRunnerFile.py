user_id = request.form.get('user_id')
  if not user_id:
      return "User ID cannot be blank", 400
   
  user_params = {
      'user_id': request.form['user_id'],
      'username': request.form['username'],
    }
  g.conn.execute(text("""
      INSERT INTO Posts_Reviews (user_id, datetime, rid, description)
      VALUES (:user_id, :datetime, :rid, :description)
      """), user_params)
  g.conn.commit()