from flask_restful import Resource,reqparse
import sqlite3


class Task(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('Detail',
                        type=str,
                        help='This field can not be blank'
                        )

    def get(self, desc):
        task = Task.get_task_by_desc(desc)
        return task, 200 if task else 404

    @classmethod
    def get_task_by_desc(cls,desc):
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()

        query = "select * from tasks where desc = ?"
        result = cursor.execute(query, (desc,))
        row = result.fetchone()

        connection.close()
        if row:
            return {"desc": row[0], "detail": row[1]}, 200 if row else 404

    @classmethod
    def insert_task(cls, task):
            connection = sqlite3.connect("todo.db")
            cursor = connection.cursor()

            query = 'INSERT INTO tasks values (?,?)'
            cursor.execute(query, (task['Desc'],task['Detail']))

            connection.commit()
            connection.close()

    @classmethod
    def update_task(cls, task):
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()

        query = "UPDATE tasks set detail = (?) where desc = ?"
        cursor.execute(query, (task['Detail'],task['Desc']))
        connection.commit()
        connection.close()


    def post(self,desc):
        if Task.get_task_by_desc(desc):
            return {"message": "task already exists"}, 400

        data = Task.parser.parse_args()
        task = {"Desc": desc, "Detail": data['Detail']}

        #try:
        Task.insert_task(task)
        #except:
            #return {"message": "An error occurred"}, 500

        return task, 201


    def put(self, desc):
        task = Task.get_task_by_desc(desc)

        data = Task.parser.parse_args()
        newtask = {"Desc": desc, "Detail": data['Detail']}

        if task:
            try:
                Task.update_task(newtask)
            except:
                {"message": "An error occurred"}, 500
        else:
            try:
                Task.insert_task(newtask)
            except:
                {"message": "An error occurred"}, 500

        return newtask

    def delete(self,desc):
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()

        query = 'DELETE from tasks where desc = ?'
        cursor.execute(query, (desc,))

        connection.commit()
        connection.close()
        return {"message": "Task deleted"}


class TaskList(Resource):
    def get(self):
        tasks = []

        connection = sqlite3.connect('todo.db')
        cursor = connection.cursor()

        query = 'select * from tasks'

        result = cursor.execute(query)

        for i in result:
            tasks.append({'desc': i[0], 'detail': i[1]})

        connection.close()
        return {"Tasks": tasks}

