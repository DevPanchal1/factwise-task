import os
import json
import requests
import psycopg2
class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
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

        self.cur.execute('''
            create table if not exists teams (
                id serial primary key,
                name varchar(64) not null unique,
                description varchar(256) not null,
                creation_time timestamp not null default now(),
                admin varchar(64) not null
            )
        ''')
        
    # create a team
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['name']) <= 64
            assert len(json_request['description']) <= 128

            self.cur.execute('''
                insert into teams (name, description, admin)
                values (%s, %s, %s)
                returning id
            ''', (json_request['name'], json_request['description'], json_request['admin']))
            return json.dumps({"id": self.cur.fetchone()[0]})

        except Exception as e:
            print(e)

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        try:
            self.cur.execute('''
                select * from teams
            ''')

            return json.dumps(self.cur.fetchall())
        except Exception as e:
            print(e)

    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        try:
            result = ""
            json_request = json.loads(request)
            self.cur.execute('''
                select * from teams 
                where id = %s
            ''', (json_request['id'],))

            return json.dumps(self.cur.fetchone())
        except Exception as e:
            print(e)

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['team']['name']) <= 64
            assert len(json_request['team']['description']) <= 128

            self.cur.execute('''
                update teams 
                set description = %s 
                where id = %s
                returning id
            ''', (json_request['description'], json_request['id']))
            return json.dumps({"id": self.cur.fetchone()[0]})

        except Exception as e:
            print(e)

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['users']) <= 50

            self.cur.execute('''
                update teams 
                set users = %s 
                where id = %s
                returning id
            ''', (json_request['users'], json_request['id']))
            return json.dumps({"id": self.cur.fetchone()[0]})

        except Exception as e:
            print(e)

    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['users']) <= 50

            self.cur.execute('''
                update teams 
                set users = %s 
                where id = %s
                returning id
            ''', (json_request['users'], json_request['id']))
            return json.dumps({"id": self.cur.fetchone()[0]})

        except Exception as e:
            print(e)

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
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