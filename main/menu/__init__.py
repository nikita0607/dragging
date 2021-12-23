<<<<<<< HEAD
import pygame

from object import Object, Button
from manager import Manager
from main import Main


class Manage(Manager):
    def draw(self, win):
        pass

    def button_click(self, button: Button):
        print("Click!")

    def start(self, main: Main):
        buttons = [Button(100, 50, 50, 50, "Test", self.button_click)]

        main.object_manager.add_objects(*buttons)

    def update(self, main: Main):
=======
import object
from manager import Manager


class Manage(Manager):
    def draw(self):
>>>>>>> bb75e844e508fc2618b32beb6c6021c543d17da2
        pass


def setup():
    return Manage()
