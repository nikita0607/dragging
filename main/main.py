import pygame
import os
import importlib

from object import *
from mouse import Mouse


class Main:
    def __init__(self):
        self.win = pygame.display.set_mode((1000, 600))
        self.mouse = Mouse()
        self.object_manager = ObjectManager(self.win)

        self.modules: dict = {}

        ignore = ["__pycache__", ".idea", "main.py", "mouse.py", "object.py", "manager.py"]
        levels = list(filter(lambda x: x not in ignore, os.listdir()))

        print(levels)

        for i in levels:
            self.modules[i] = __import__(i).setup()

        self.current_module = self.modules["menu"]
        self.current_module.start(self)

    def draw(self):
        self.win.fill((60, 0, 0))

        self.object_manager.draw()

        pygame.display.update()

    def run(self):

        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.mouse.update()
            self.current_module.update(self)

            if self.mouse.left_pressed:
                if not self.mouse.is_drag:
                    self.object_manager.find_collusion_with_mouse(self.mouse)
                else:
                    self.object_manager.drag(self.mouse)
            elif self.mouse.is_click:
                self.object_manager.click(self.mouse)

            self.draw()
            pygame.time.delay(30)

        pygame.quit()


if __name__ == '__main__':
    pygame.font.init()
    pygame.init()

    main = Main()

    main.object_manager.add_object(RectObject(50, 50, 10, 100))
    main.object_manager.add_object(RectObject(200, 50, 100, 100, (5, 120, 14)))

    main.run()