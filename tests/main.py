import unittest
from os import path

from yaml.tokens import ValueToken
from core.pundit.pundit import Pundit
from core.validator.validator import Validator

tester = Pundit()

class User:
    self.id = 1111
    self.name = "lalla"

class testPundit:
    def __init__(tester, user):
        self.tester = tester
        self.user = user
        self.testuser = User()

        self.tester.register(user=user)
        tester.register(user=user)
        self.tester.getName(id_=testuser.id)
        self.tester.evaluate(user=testuser, link="https://bashupload.com/aFiur/submission.zip", ticket="001_aeivub_aqeorequb")

        

testuser = User()
testPundit(tester, testuser)


class InequalityTest(unittest.TestCase):
    self.validator = Validator
    self.pundit = Pundit()
    self.usersubs = 1
    self.ticket = "rebetbbe"
    def testEqual(self):
        report = self.Validator(
                    submission=self.ticket,
                    filename=path.join("/tmp/master", "testuser", "{}_{}/tasks.zip"
                                           .format(
                                               str(self.usersubs+1).zfill(3),
                                               self.ticket
                                           )),
                    user="testuser",
                    subs=self.usersubs+1,
                    tmp="/tmp/master/tempdirectory"
                ).validate()
        self.failUnlessEqual(report, {"report": {"tasks": [{"testtask1": True}, {"testtask2": False}]}})


        self.testEqual(self.pundit.leaderboard(count=2), [("testuser1", 200), ("testuser2", 170)])
        self.testEqual(self.pundit.solvedbyuser(param=0), ["testtask1", "testtask2"])

if __name__ == '__main__':
    unittest.main()
