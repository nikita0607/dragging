import pygame


class Mouse:
    def __init__(self):
        self.pos = self.last_pos = pygame.mouse.get_pos()
        self.pressed = self.last_pressed = pygame.mouse.get_pressed(3)

        self.last_dragged = 0
        self.is_dragging = False

        self.is_hold = False
        self.is_click = False
        self.is_drag = False

<<<<<<< HEAD
        self.last_drag = False
        self.last_click = False
        self.last_hold = False

=======
>>>>>>> bb75e844e508fc2618b32beb6c6021c543d17da2
    def update(self):
        self.last_pressed = self.pressed
        self.pressed = pygame.mouse.get_pressed(3)

        self.last_pos = self.pos
        self.pos = pygame.mouse.get_pos()

<<<<<<< HEAD
        if self.last_pressed[0] == 1 and self.pressed[0] == 1:
            self.is_drag = self.is_hold and self.pos != self.last_pos or self.is_drag
            self.is_hold = not self.is_drag

        elif self.is_hold and self.last_pressed[0] == 1:
=======
        if self.last_pressed[0] == self.pressed[0]:
            if self.is_hold and self.pos != self.last_pos:
                self.is_hold = False
                self.is_drag = True
            else:
                self.is_hold = True

        elif self.is_hold and self.last_pressed[0] == self.pressed[0]: 
>>>>>>> bb75e844e508fc2618b32beb6c6021c543d17da2
            self.is_hold = False
            self.is_click = True

        else:
            self.is_hold = False
<<<<<<< HEAD
            self.is_drag = False
            self.is_click = False
=======
>>>>>>> bb75e844e508fc2618b32beb6c6021c543d17da2

    @property
    def left_pressed(self) -> bool:
        return self.pressed[0]

    def get_drag_shift(self) -> tuple:
        return self.pos[0] - self.last_pos[0], self.pos[1] - self.last_pos[1]
