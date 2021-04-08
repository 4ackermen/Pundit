from core.pundit.pundit import Pundit

pun = Pundit()

pun.register("PunditTest")
pun.getName(0)
