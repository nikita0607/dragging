from typing import Union

import pygame

from abc import ABC, abstractmethod
from mouse import Mouse
from main import Main


main: Main = None


def init(_main: Main):
    global main

    main = _main


class Object(ABC):
    def __init__(self, obj, surface, color: pygame.Color | tuple[int, int, int] = (255, 255, 255)):
        self.obj = obj
        self.surface = surface
        self.color = color

    def click(self, mouse: Mouse, type):
        pass

    def drag(self, mouse: Mouse, dragging_shift):
        pass

    def hold(self, mouse: Mouse):
        pass

    @abstractmethod
    def draw(self, win):
        win.blit(self.surface, self.obj)

    @abstractmethod
    def collide_with_cords(self, x, y) -> bool:
        pass

    @abstractmethod
    def move(self, x, y):
        pass

    def __str__(self):
        return f"Object(surface: {self.surface}, obj: {self.obj}"

    @property
    @abstractmethod
    def position(self):
        pass


class EmptyObject(Object):
    def __init__(self):
        super().__init__(None, None)

    def draw(self, win):
        pass

    @property
    def position(self):
        return 0, 0

    def move(self, x, y):
        pass

    def collide_with_cords(self, x, y) -> bool:
        return True


class RectObject(Object):
    def __init__(self, x, y, width, height, color=pygame.color.Color(255, 255, 2)):
        surface = pygame.Surface((width, height))
        surface.fill(color)

        super().__init__(pygame.Rect(x, y, width, height), surface)

        self.x, self.y, self.width, self.height = x, y, width, height

    def click(self, mouse: Mouse, type: int):
        if type == 1:
            main.object_manager.move_object_up(self)

        print("Click")

    def draw(self, win):
        super().draw(win)

    def drag(self, mouse, dragging_shift):
        self.move(mouse.pos[0] + dragging_shift[0], mouse.pos[1] + dragging_shift[1])

    def collide_with_cords(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.obj.x, self.obj.y = x, y
        self.x, self.y = x, y

    @property
    def position(self):
        return self.x, self.y


class Button(RectObject):
    def __init__(self, x, y, width, height, text, callback, color=pygame.color.Color(255, 255, 2)):
        super().__init__(x, y, width, height, color)
        self.callback = callback
        self.text = text

    def click(self, mouse: Mouse, type: int):
        self.callback(self)

    def drag(self, mouse, dragging_shift):
        pass


class ObjectManager:
    def __init__(self, win):
        self.objects: list[Object] = []

        self.find_dragged_obj: bool = False
        self.last_finded_obj_id = -1
        self.dragging_shift = (0, 0)

        self.win = win
        self.empty_object = EmptyObject()

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def add_objects(self, objs: list):
        for obj in objs:
            self.add_object(obj)

    def move_object_up(self, obj: Union[Object, int]):
        if isinstance(obj, Object):
            obj = self.objects.index(obj)

        self.objects.append(self.objects.pop(obj))

    def find_collusion_with_mouse(self, mouse, move_up: bool = False):
        for _id in range(1, len(self.objects) + 1):
            obj = self.objects[-_id]

            if obj.collide_with_cords(*mouse.pos):
                self.last_finded_obj_id = len(self.objects) - _id
                self.dragging_shift = (obj.position[0] - mouse.pos[0], obj.position[1] - mouse.pos[1])
                if move_up:
                    self.objects.append(self.objects.pop(-_id))
                    self.last_finded_obj_id = len(self.objects) - 1
                return obj

        self.last_finded_obj_id = -1

        return self.empty_object

    def drag(self, mouse: Mouse) -> None:
        if self.last_finded_obj_id != -1:
            self.objects[self.last_finded_obj_id].drag(mouse, self.dragging_shift)

    def hold(self, mouse: Mouse):
        if self.last_finded_obj_id != -1:
            self.objects[self.last_finded_obj_id].hold(mouse)

    def click(self, mouse: Mouse, type: int = 0) -> None:
        self.find_collusion_with_mouse(mouse).click(mouse, type)

    def draw(self):
        for obj in self.objects:
            obj.draw(self.win)