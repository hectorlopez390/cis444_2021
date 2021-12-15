from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.logging import logger
from db_con import get_db_instance, get_db
import bcrypt



def handle_request():
    logger.debug("Create Handle Request")
    cur = g.db.cursor()
    cur.execute("Select * from users where username = '"+ request.form['username']+ "';" )
    user = cur.fetchone()
    if user == None:
        salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
        cur.execute("insert into users (username, salted_pass) values ('" + request.form['username'] + "', '" + salted.decode('utf-8') + "');")
        print("sign up complete")
        cur.close()
        g.db.commit()
        return json_response(message = "success")
    else:
        return json_response(message = "failure")
