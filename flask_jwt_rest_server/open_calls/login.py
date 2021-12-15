from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt
from db_con import get_db_instance, get_db



def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }

    cur = g.db.cursor()
    cur.execute("select * from users where username = '" + user['sub'] + "';")
    credentials = cur.fetchone()
    cur.close()

    if credentials is None:
        logger.debug("no users found")
        return json_response(status_=401, message = "no users found", authenticated = False)
    else:
        if bcrypt.checkpw(bytes(password_from_user_form, 'utf-8'), bytes(credentials[2], 'utf-8')) == True:
            logger.debug("Login successful, user " + request.form['username'] + " found")
            return json_response(token = create_token(user), authenticated = True)
        else:
            return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
