import mysql.connector
from shutil import copy
from tempfile import TemporaryDirectory as mktemp
from core.pundit.helpers import (
    unzip
)
from os import (
    mkdir,
    listdir,
    path,
    rename
)
from yaml import (
    safe_load
)
from urllib.request import (
    urlretrieve,
    URLError
)

with open("config.yaml", 'r') as file:
    CONFIG = safe_load(file)
    STORAGE = CONFIG['storage']
    PUNDIT = CONFIG['pundit']


class Pundit:
    def __init__(self):
        self.master = STORAGE['master']
        "" if path.exists(self.master) else mkdir(self.master)
        "" if path.exists(path.join(self.master, 'byusers')) else mkdir(
            path.join(self.master, 'byusers'))

    def register(self, user):
        name = str(user)
        userid = 0  # str(user.id)
        if STORAGE['db_pass'] == "test":
            print("Testing")
        else:
            cnx = mysql.connector.connect(
                host="localhost",
                user=STORAGE['db_user'],
                password=STORAGE['db_pass'],
                database=STORAGE['database'],
                auth_plugin='mysql_native_password'
            )
            cursor = cnx.cursor()
            userpath = name.split("#")[0] + userid
            cursor.execute(
                'SELECT * from users where userid="{}"'.format(userid))
            _ = cursor.fetchall()
            if(len(_)):
                return "Hello {user}, looks like you've already registered. If you think this a mistake, please ping any of the admins.".format(user=name.split("#")[0])
            else:
                reg = ("INSERT INTO users"
                       "(name, userid,userpath)"
                       "VALUES (%s, %s, %s)")
                cursor.execute(reg, (name, userid, userpath))
                cnx.commit()
                cnx.close()
                return "Successfully Registered!!"

    def getName(self, id_=''):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT name from users where userid={}".format(id_[0]))
        try:
            name = cursor.fetchone()[0].split('#')[0]
        except:
            return None
        cnx.close()
        return name

    def evaluate(self, user, link, ticket):
        tmp = mktemp()
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT userpath from users where userid={}".format(str(user.id)))
        userpath = cursor.fetchone()[0]
        "" if path.exists(path.join(self.master, 'byusers', userpath)) else mkdir(
            path.join(self.master, 'byusers', userpath))
        usersubs = len(listdir(path.join(self.master, 'byusers', userpath)))
        try:
            urlretrieve(
                link,
                path.join(tmp.name, "tasks.zip")
            )
            unzip(
                path.join(tmp.name, "tasks.zip"),
                tmp.name,
            )

            if(len(listdir(tmp.name)) > 0):
                mkdir(path.join(self.master, 'byusers', userpath, "{}_{}"
                                .format(
                                    str(usersubs+1).zfill(3),
                                    ticket
                                )))
                mkdir(path.join(tmp.name, "templates"))
                copy(
                    path.join(tmp.name, "tasks.zip"),
                    path.join(tmp.name, "templates", "tasks.zip")
                )
                rename(
                    path.join(tmp.name, "tasks.zip"),
                    path.join(self.master, 'byusers', userpath, "{}_{}/tasks.zip"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      ticket
                                  )))
                unzip(
                    path.join(self.master, 'byusers', userpath, "{}_{}/tasks.zip"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      str(ticket)
                                  )),
                    path.join(self.master, 'byusers', userpath, "{}_{}/"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      str(ticket)
                                  ))
                )
            else:
                return(
                    False,
                    "Please submit one or more solution!!"
                )

        except Exception as e:
            print(e)

    def solvedbyuser(self, param):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        if(type(param) == int):
            execute = "SELECT tasks from users where userid={}".format(param)
        else:
            execute = "SELECT tasks from users where name={}".format(
                repr(param))
        cursor = cnx.cursor()
        cursor.execute(execute)
        try:
            solved = list(map(lambda x: x[0], eval(cursor.fetchone()[0])))
        except:
            solved = None
        cnx.close()
        return solved

    def leaderboard(self, count=3, all=False):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT userid, score from users ORDER BY score DESC, entropy")
        board = cursor.fetchall()
        cnx.close()
        return board if all else board[:count]

    def firstbloods(self):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT name, tasks from users ORDER BY score DESC, entropy")
        data = cursor.fetchall()
        data = list(map(lambda data: (data[0], eval(data[1])), data))
        """
        data = [('userid', [('task1', 'timestamp'), ('task2', 'timestamp2')]), ('userid2', [('task1', 'timestamp'), ('task2', 'timestamp2')])...]
        """
        bloods = {}
        for task in TASKS:
            solved = []
            for entry in data:
                """
                data = [('userid', [('task1', 'timestamp'), ('task2', 'timestamp2')]), ('userid2', [('task1', 'timestamp'), ('task2', 'timestamp2')])...]
                """
                if(any(t[0] == task for t in entry[1])):
                    solved.append((
                        entry[0],
                        int(list(filter(None,
                                        list(map(
                                            lambda submission, task: submission[1] if submission[0] == task else None,
                                            entry[1],
                                            [task for _ in range(
                                                len(entry[1]))]
                                        ))))[0]
                            )
                    ))
            if(solved):
                bloods[task] = sorted(
                    solved, key=lambda x: x[1])[0]
            else:
                bloods[task] = None
        return bloods
