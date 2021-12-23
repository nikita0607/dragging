import pygame

from abc import ABC, abstractmethod
from mouse import Mouse


class Object(ABC):
    def __init__(self, obj, surface, color: pygame.Color | tuple[int, int, int] = (255, 255, 255)):
        self.obj = obj
        self.surface = surface
        self.color = color

    def click(self, mouse: Mouse):
        pass

    def end_click(self):
        pass

    def start_drag(self, mouse, collusion_cord):
        pass

    def drag(self, mouse):
        pass

    def end_drag(self):
        pass

    def hold(self, mouse):
        pass

    def end_hold(self):
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

        self.drag_shift = []

    def click(self, mouse: Mouse):
        pass

    def draw(self, win):
        super().draw(win)

    def start_drag(self, mouse, collusion_cords):
        self.drag_shift = self.position[0] - collusion_cords[0], self.position[1] - collusion_cords[1]

    def drag(self, mouse):
        self.move(mouse.pos[0] + self.drag_shift[0], mouse.pos[1] + self.drag_shift[1])

    def collide_with_cords(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.obj.x, self.obj.y = x, y
        self.x, self.y = x, y

    @property
    def position(self):
        return self.x, self.y


class Button(Object):
    def move(self, x, y):
        pass

    def collide_with_cords(self, x, y) -> bool:
        return self.x <= x <= self.x + self.size[0] and self.y <= self.size[1] <= self.y + self.size[1]

    def __init__(self, width: int, height: int, x: int, y: int, text: str,
                 callback=None, color: pygame.Color | tuple[int, int, int] = (0, 0, 0)):
        self.size = (width, height)
        self.x = x
        self.y = y

        self.text = text

        self.callback = callback

        self.clicked = False

        obj = pygame.Rect(x, y, width, height)
        super().__init__(obj, pygame.Surface(self.size), color)

    def draw(self, win: pygame.Surface):
        win.blit(self.surface, self.obj)

    def click(self, mouse: Mouse):
        self.callback(self)

    def hold(self, mouse):
        if self.clicked: return
        self.clicked = True
        self.callback(self)

    def end_hold(self):
        self.clicked = False

    @property
    def position(self):
        return self.x, self.y


class ObjectManager:
    def __init__(self, win):
        self.objects: list[Object] = []

        self.find_collide_obj: bool = False
        self.collide_object = None
        self.dragging_shift = (0, 0)

        self.win = win
        self.empty_object = EmptyObject()

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def add_objects(self, *objects):
        for obj in objects:
            self.add_object(obj)

    def find_collusion_with_mouse(self, mouse):
        for _id in range(1, len(self.objects) + 1):
            obj = self.objects[-_id]

            if obj.collide_with_cords(*mouse.last_pos):
                obj.start_drag(mouse, mouse.last_pos)
                self.find_collide_obj = True
                self.collide_object = obj
                return obj

        self.find_collide_obj = False

        return self.empty_object

    def drag(self, mouse: Mouse) -> None:
        if self.find_collide_obj:
            self.collide_object.drag(mouse)

    def end_drag(self):
        if not self.find_collide_obj: return
        self.collide_object.end_drag()
        self.find_collide_obj = False

    def end_click(self):
        if not self.find_collide_obj: return
        self.collide_object.end_click()

    def end_hold(self):
        if not self.find_collide_obj: return
        self.collide_object.end_hold()

    def click(self, mouse: Mouse) -> None:
        self.find_collusion_with_mouse(mouse).click(mouse)

    def draw(self):
        for obj in self.objects:
            obj.draw(self.win)