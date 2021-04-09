import mysql.connector
from shutil import copy
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
