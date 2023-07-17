import pygame

class Paddle:
    PADDLE_COLOR = (255, 255, 255)
    PADDLE_VELOCITY = 5

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.init_x = x
        self.init_y = y
        self.width = width
        self.height = height

    def move(self, direction):
        if direction == "up":
            self.y -= self.PADDLE_VELOCITY
        elif direction == "down":
            self.y += self.PADDLE_VELOCITY
    
    def render(self, frame):
        pygame.draw.rect(frame, self.PADDLE_COLOR, (self.x, self.y, self.width, self.height))

    def clamp(self, frame_height):
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > frame_height:
            self.y = frame_height - self.height

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
