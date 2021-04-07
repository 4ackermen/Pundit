import mysql.connector
from os import (
    mkdir,
    path
)
from yaml import (
    safe_load
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
