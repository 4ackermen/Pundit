from time import sleep
import sys
from base64 import b64encode
from glob import glob
from os import (
    path,
    mkdir,
    chdir,
    remove,
    system,
    environ as ENV,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    gethostname,
    gethostbyname,
)
from sys import executable
from time import sleep
from zipfile import ZipFile

# todo: dump pwn and use subprocess with pipe
from pwn import process
from yaml import SafeLoader, load

with open("tasks.yaml", 'r') as file:
    TASKS = load(file, Loader=SafeLoader)

# if(sys.argv[1]!='tester'): remove("tasks.yaml") # make sure users cant read the testcases


def safeopen(file):
    if(path.exists(file)):
        """
        task/task.py
        """
        return open(file)
    elif(path.exists(file+file.split(".")[-1])):
        """
        task/task.py.py | task/task.c.c
        """
        return open(file+file.split(".")[-1])
    else:
        """
        task/<None>
        """
        return False


def listtasks():
    mkdir("tasks")
    with ZipFile("tasks.zip", 'r') as refer:
        refer.extractall("tasks")
    return list(map(lambda x: x.split("/")[1],  glob("tasks/*/*.[pcfa]*")))


def gethost():
    try:
        checker = gethostbyname(gethostname()).split(".")
        checker[-1] = '1'
        return '.'.join(checker)
    except:
        return "192.168.64.1"


def profanitycheck(task):
    file = "tasks/%s/%s.py" % (task, task)
    allowed = TASKS[task]['allowed']
    blacklist = ["__import__", "import", "os", "system",
                 "socket", "subprocess", "glob", "sys", "open"]
    fd = safeopen(file)
    if(fd):
        code = fd.readlines()
    else:
        return False
    for word in blacklist:
        if(any(word in line for line in code)):
            if(any(_word in line for line in code for _word in allowed)):
                pass
            else:
                return True
    open("flag.txt", 'w').write(b64encode(
        b"Hello, If you are seeing this, please be responsible and contact one of the admins regarding this.").decode())
    return False


def checklines(task):
    maxlines = TASKS[task]['maxlines']
    try:
        lines = len(safeopen("tasks/%s/%s.%s" % (task, task, TASKS[task]['language'][:2])).readlines())
    except AttributeError:
        return False
    if(maxlines == 0):
        return False
    if(lines > maxlines):
        return True
    else:
        return False


def retproc(task, lang):
    if(lang == "python"):
        io = process([executable, "tasks/%s/%s.py" % (task, task)])
        return True, io
    else:
        flags = TASKS[task]['flags']
        ret = system(
            "gcc %s tasks/%s/%s.c -o tasks/%s/%s.out"
            % (" ".join(flags), task, task, task, task)
        )
        return (
            (False, 3) if ret != 0 else (
                True, process("tasks/%s/%s.out" % (task, task)))
        )


def checkcases(task, lang):
    delimiter = TASKS[task]['delimiter']
    cases = TASKS[task]['testcases']
    if(lang == "python" and profanitycheck(task)):
        return (
            False,
            "Operation not permitted!!",
        )
    if(checklines(task)):
        return (
            False,
            "Number of lines exceeeded!!"
        )
    casereturns = {'passed': [], 'failed': []}
    for index, _input, _output in zip(range(len(cases['input'])), cases['input'], cases['output']):
        d = retproc(task, lang)
        ret = d[0]
        io = d[1]
        if(not io):
            return (
                False,
                "fatal",
            )
        elif(ret == 2):
            return (
                False,
                "objfail",
            )
        elif(ret == 3):
            return (
                False,
                "compfail",
            )
        else:
            pass
        print("Checking testcase, {}:{}".format(delimiter.join(
            list(map(str, _input))), delimiter.join(list(map(str, _output)))))
        if _input:
            io.sendline(delimiter.join(list(map(str, _input))))
        sleep(0.5)
        try:
            test = io.recv(timeout=8).decode().rstrip()
        except EOFError:
            test=''            
        if(test == ''):
            casereturns['failed'].append(
                (
                    index,
                    False,
                    "Timeout",
                    delimiter.join(list(map(str, _input)))
                )
            )
        elif(test != delimiter.join(list(map(str, _output)))):
            casereturns['failed'].append(
                (
                    index,
                    False,
                    "wrong",
                    {
                        delimiter.join(list(map(str, _input))):
                        test
                    }
                )
            )
        else:
            casereturns['passed'].append(
                (
                    index,
                    True,
                    "passed"
                )
            )

    return casereturns


def checktask(task):
    try:
        rules = TASKS[task]
    except KeyError:
        return (False, "Task did not match any :(")
    if(rules['flageval']):
        if(
            open(
                "tasks/{}/{}.flag"
                .format(task, task)
            ).read().rstrip() == rules['flag']
        ):
            return (
                (True, "pass")
                if path.exists(
                    "tasks/{}/{}.txt"
                    .format(task, task)
                )
                else (False, "No Solution Provided")
            )
        else:
            print(
                "Wrong flag, {} expected: {}"
                .format(
                    open("tasks/{}/{}.flag".format(task, task)).read(),
                    rules['flag']
                )
            )
            return (
                False,
                "Wrong Flag"
            )
    else:
        lang = TASKS[task]['language']
        return checkcases(task, lang)


def checkall():
    report = {
        'tasks':
        {}
    }
    byuser = listtasks()
    for i in byuser:
        try:
            report['tasks'][i] = checktask(i.lower())
        except Exception as e:
            report['tasks'][i] = (False, "Error running the script!")
            print(e)
    return report


def send(data):
    io = socket(AF_INET, SOCK_STREAM)
    io.connect((gethost(), int(ENV['VPORT'])))
    report['submission_id'] = ENV['SUBMISSION_ID']
    io.send((str(len(repr(report))).ljust(8)).encode())
    io.send(repr(report).encode())


if __name__ == "__main__":
    report = checkall()
    print(report) if sys.argv[1] == 'debug' else send(report)
    print(report)
    exit(0)
