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
