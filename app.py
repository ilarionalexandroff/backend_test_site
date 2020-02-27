from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
import sqlite3
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app)
api = Api(app)


class User(Resource):

    def get(self, id=0):
        if id == 0:
            return "Please specify user id", 400

        conn = sqlite3.connect("my_db.db")
        cursor = conn.cursor()

        select_email = "select email from users where id = " + str(id)
        cursor.execute(select_email)
        email = str(cursor.fetchone())
        # Here I remove not needed symbols from string with email (need to import "re" library):
        email = re.sub(r"[(',)]", "", email)

        select_description = "select description from users where id = " + str(id)
        cursor.execute(select_description)
        description = str(cursor.fetchone())
        # Here I remove not needed symbols from string with description
        description = description[2:-3]

        response = {"email":email, "description":description}


        return response, 200


api.add_resource(User, "/user", "/user/", "/user/<int:id>")

class UserStatus(Resource):

    def get(self, id=0):
        if id == 0:
            return "Please specify user id", 400
        conn = sqlite3.connect("my_db.db")
        cursor = conn.cursor()
        select_query = "select status from user_statuses where user_id=" + str(id)
        cursor.execute(select_query)
        output = str(cursor.fetchall())

        if "Online" in output:
             status = "Online"
        elif "Offline" in output:
            status = "Offline"
        else:
            status = "--"
        response = {"user_id":id, "status": status}

        return response, 200

    def post(self, id):
        parser = reqparse.RequestParser()
        # parser.add_argument("user_id")
        parser.add_argument("status")
        params = parser.parse_args()

        # user_id = params["user_id"]
        user_status = params["status"]

        conn = sqlite3.connect("my_db.db")
        cursor = conn.cursor()
        update_query = "update user_statuses set status=\'" + str(user_status) + "\' where user_id=" + str(id)
        cursor.execute(update_query)
        conn.commit()

        select_query = "select status from user_statuses where user_id=" + str(id)
        cursor.execute(select_query)

        output = str(cursor.fetchall())
        if user_status in output:
            message = "User status successfully changed to " + user_status
            response = {"result": message}
            return response, 201
        else:
            message = "Something went wrong. Status not changed"
            response = {"result": message}
            return response, 400


api.add_resource(UserStatus, "/user_status", "/user_status/", "/user_status/<int:id>")


if __name__ == '__main__':
    app.run(debug=True)