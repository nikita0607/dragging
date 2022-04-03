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

        main.object_manager.add_objects(buttons)

    def update(self, main: Main):
        pass


def setup():
    return Manage()
