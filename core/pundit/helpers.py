from zipfile import (
    BadZipFile,
    ZipFile,
)


def unzip(file, topath):
    with ZipFile(file, 'r') as refer:
        refer.extractall(topath)
