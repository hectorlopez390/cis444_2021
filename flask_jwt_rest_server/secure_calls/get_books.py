from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import json

from tools.logging import logger


def handle_request():
    logger.debug("Get Books Handle Request")

    cur = g.db.cursor()
    cur.execute("select * from books;")
    allBooks = cur.fetchall()
    cur.close()

    theBooks = '{"books": ['
    for r in allBooks:
        if r[0] < len(allBooks):
            theBooks += '{"id": "' +str(r[0]) + '","title": "' + str(r[1]) + '", "price": "' + str(r[2]) + '"},'
        else:
            theBooks += '{"id": "' +str(r[0]) + '","title": "' + str(r[1]) + '", "price": "' + str(r[2]) + '"}'
    theBooks += "]}"
    logger.debug(theBooks)
    
    return json_response( token = create_token(  g.jwt_data ) , data = json.loads(theBooks))

