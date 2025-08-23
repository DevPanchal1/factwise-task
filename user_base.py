import os
import json
import requests
import psycopg2
class UserBase:
    """
    Base interface implementation for API's to manage users.
    """
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('host'),
            port=os.getenv('port'),
            user=os.getenv('user'),
            password=os.getenv('pass'),
            database=os.getenv('db')
        )
        self.cur = self.connection.cursor()

        # create users table if it doesn’t exist
        self.cur.execute('''
            create table if not exists users (
                id serial primary key,
                name varchar(64) not null unique,
                display_name varchar(64) not null
            )
        ''')
    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        try:
            json_request = json.loads(request)

            self.cur.execute('''
                insert into users (name, display_name) 
                values (%s, %s) 
                returning id
            ''', (json_request['name'], json_request['display_name']))

            return json.dumps({"id": self.cur.fetchone()[0]})
        except Exception as e:
            print(e)

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        self.cur.execute('''
            select * from users
        ''')
        return json.dumps(self.cur.fetchall())

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        try:
            json_request = json.loads(request)
            self.cur.execute('''
                select * from users 
                where id = %s
            ''', (json_request['id'],))

            return json.dumps(self.cur.fetchone())
        except Exception as e:
            print(e)

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        try:
            json_request = json.loads(request)

            self.cur.execute('''
                update users 
                set display_name = %s 
                where id = %s
                returning id
            ''', (json_request['display_name'], json_request['id']))

            return json.dumps({"id": self.cur.fetchone()[0]})
        except Exception as e:
            print(e)

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        try:
            json_request = json.loads(request)
            self.cur.execute('''
                select * 
                from users 
                join teams on users.id = teams.user_id 
                where users.id = %s
            ''', (json_request['id'],))

            return json.dumps(self.cur.fetchall())
        except Exception as e:
            print(e)