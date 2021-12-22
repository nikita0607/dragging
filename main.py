from abc import ABC, abstractmethod
import pygame


class Mouse:
    def __init__(self):
        self.pos = self.last_pos = pygame.mouse.get_pos()
        self.pressed = self.last_pressed = pygame.mouse.get_pressed(3)

    def update(self):
        self.last_pos = self.pos
        self.pos = pygame.mouse.get_pos()

        self.last_pressed = self.pressed
        self.pressed = pygame.mouse.get_pressed(3)

    @property
    def left_pressed(self) -> bool:
        return self.pressed[0]

    @property
    def is_dragging(self) -> bool:
        return self.last_pressed[0] == self.pressed[0]

    def get_drag_shift(self) -> tuple:
        return self.pos[0] - self.last_pos[0], self.pos[1] - self.last_pos[1]


class Object(ABC):
    def __init__(self, obj, surface, color: pygame.Color | tuple[int, int, int] = (255, 255, 255)):
        self.obj = obj
        self.surface = surface
        self.color = color
    
    @abstractmethod
    def draw(self):
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


class RectObject(Object):
    def __init__(self, x, y, width, height, color=pygame.color.Color(255, 255, 2)):
        surface = pygame.Surface((width, height))
        surface.fill(color)

        super().__init__(pygame.Rect(x, y, width, height), surface)

        self.x, self.y, self.width, self.height = x, y, width, height

    def draw(self):
        super().draw()

    def collide_with_cords(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.obj.x, self.obj.y = x, y
        self.x, self.y = x, y

    @property
    def position(self):
        return self.x, self.y


class ObjectManager:
    def __init__(self):
        self.objects: list[Object] = []

        self.find_dragged_obj: bool = False
        self.dragging_shift = (0, 0)

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def select_dragged_object(self, mouse):
        for _id in range(1, len(self.objects) + 1):
            obj = self.objects[-_id]

            if obj.collide_with_cords(*mouse.pos):
                self.find_dragged_obj = True
                self.dragging_shift = (obj.position[0] - mouse.pos[0], obj.position[1] - mouse.pos[1])
                self.objects.append(self.objects.pop(-_id))
                return obj

        self.find_dragged_obj = False

    def drag_object(self, mouse: Mouse) -> None:
        if self.find_dragged_obj:
            self.objects[-1].move(mouse.pos[0]+self.dragging_shift[0], mouse.pos[1]+self.dragging_shift[1])

    def draw(self):
        for obj in self.objects:
            obj.draw()


win = pygame.display.set_mode((1000, 600))
mouse = Mouse()
object_manager = ObjectManager()


def draw():
    win.fill((60, 0, 0))

    object_manager.draw()

    pygame.display.update()


object_manager.add_object(RectObject(50, 50, 10, 100))
object_manager.add_object(RectObject(200, 50, 100, 100, (5, 120, 14)))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse.update()

    if mouse.left_pressed:
        if not mouse.is_dragging:
            object_manager.select_dragged_object(mouse)
        else:
            object_manager.drag_object(mouse)

    draw()
    pygame.time.delay(30)

pygame.quit()
