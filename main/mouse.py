import pygame


class Mouse:
    def __init__(self):
        self._hold_counter = 0
        self._hold_counter_r = 0

        self.pos = self.last_pos = pygame.mouse.get_pos()
        self.pressed = self.last_pressed = pygame.mouse.get_pressed(3)

        self.last_dragged = 0
        self.is_dragging = False

        self.is_hold = False
        self.is_click = False
        self.is_drag = False

        self.is_click_r = False
        self.is_hold_r = False

        self.last_drag = False
        self.last_click = False
        self.last_hold = False

    def update(self):
        self.last_pressed = self.pressed
        self.pressed = pygame.mouse.get_pressed(3)

        self.last_pos = self.pos
        self.pos = pygame.mouse.get_pos()

        if self.last_pressed[0] == 1 and self.pressed[0] == 1:
            self._hold_counter += 1

            if self._hold_counter > 8 or self._hold_counter and self.pos != self.last_pos:
                self.is_drag = self.is_hold and self.pos != self.last_pos or self.is_drag
                self.is_hold = not self.is_drag
                self.is_click = False

        elif self.last_pressed[0] == 1 and self.pressed[0] == 0 and not (self.is_drag or self.is_hold):
            self.is_click = True

        else:
            self._hold_counter = 0
            self.is_hold = False
            self.is_drag = False
            self.is_click = False

        if self.last_pressed[2] == 1 and self.pressed[2] == 1:
            self._hold_counter_r += 1

            if self._hold_counter_r > 8:
                self.is_hold_r = True

        elif self.last_pressed[2] == 1 and self.pressed[2] == 0 and not self.is_hold_r:
            self.is_click_r = True

        else:
            self._hold_counter_r = 0
            self.is_hold_r = False
            self.is_click_r = False

    @property
    def left_pressed(self) -> bool:
        return bool(self.pressed[0])

    @property
    def right_pressed(self) -> bool:
        return bool(self.pressed[1])

    def get_drag_shift(self) -> tuple:
        return self.pos[0] - self.last_pos[0], self.pos[1] - self.last_pos[1]
