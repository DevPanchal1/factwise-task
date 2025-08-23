import os
import json
import requests
import psycopg2
class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
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
          create table if not exists project_boards (
              id serial primary key,
              name varchar(64) not null,
              description varchar(128) not null,
              team_id integer not null,
              creation_time timestamp not null
          )
      ''')

    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['name']) <= 64
            assert len(json_request['description']) <= 128

            self.cur.execute('''
                insert into project_boards (name, description, team_id, creation_time) 
                values (%s, %s, %s, %s) 
                returning id
            ''', (
                json_request['name'], 
                json_request['description'], 
                json_request['team_id'],
                json_request['creation_time']
            ))

            return json.dumps({"id": self.cur.fetchone()[0]})

        except Exception as e:
            print(e)

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        try:
            json_request = json.loads(request)

            self.cur.execute('''
                update project_boards 
                set status = %s 
                where id = %s
                returning id
            ''', (
                json_request['status'], 
                json_request['id']
            ))

            return json.dumps({"id": self.cur.fetchone()[0]})
        except Exception as e:
            print(e)

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        try:
            json_request = json.loads(request)

            assert len(json_request['title']) <= 64
            assert len(json_request['description']) <= 128

            self.cur.execute('''
                insert into tasks (title, description, user_id, creation_time) 
                values (%s, %s, %s, %s) 
                returning id
            ''', (
                json_request['title'], 
                json_request['description'], 
                json_request['user_id'],
                json_request['creation_time']
            ))

            return json.dumps({"id": self.cur.fetchone()[0]})
        except Exception as e:
            print(e)

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        try:
            json_request = json.loads(request)

            self.cur.execute('''
                update tasks 
                set status = %s 
                where id = %s
                returning id, status
            ''', (
                json_request['status'], 
                json_request['id']
            ))

            row = self.cur.fetchone()
            self.connection.commit()

            if row:
                return json.dumps({"id": row[0], "status": row[1]})
            else:
                return json.dumps({"error": "Task not found"})

        except Exception as e:
            print(e)
            return json.dumps({"error": str(e)})

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        try:
            json_request = json.loads(request)

            self.cur.execute('''
                select * 
                from project_boards 
                where id = %s
            ''', (json_request['id'],))

            return json.dumps(self.cur.fetchone())
        except Exception as e:
            print(e)

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        try:
            result = ""
            json_request = json.loads(request)

            self.cur.execute('''
                select * 
                from project_boards 
                where id = %s
            ''', (json_request['id'],))

            out_file = open("output.txt", "w")
            out_file.write(json.dumps(self.cur.fetchone()))

        except Exception as e:
            print(e)
