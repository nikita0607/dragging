import object
from manager import Manager


class Manage(Manager):
    def draw(self):
        pass


def setup():
    return Manage()
