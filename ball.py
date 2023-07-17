import pygame

class Ball:
    BALL_COLOR = (255, 255, 0)
    MAX_VELOCITY = 5

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.v_x = self.MAX_VELOCITY
        self.v_y = 0

    def render(self, frame):
        pygame.draw.circle(frame, self.BALL_COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
