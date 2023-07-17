import pygame
from paddle import Paddle
from ball import Ball
from handle_key_pressed import handle_key_pressed

# init game
pygame.init()

FRAME_WIDTH, FRAME_HEIGHT = 700, 500
FPS = 60

FRAME = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
pygame.display.set_caption("Ping Pong AI")

# paddles
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_PADDING = 30, 150, 10

# ball
BALL_RADIUS = 10

left_paddle = Paddle(
        PADDLE_PADDING,
        FRAME_HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )
right_paddle = Paddle(
        FRAME_WIDTH - PADDLE_WIDTH - PADDLE_PADDING,
        FRAME_HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )
play_ball = Ball(FRAME_WIDTH // 2, FRAME_HEIGHT // 2, BALL_RADIUS)

def draw(frame, paddles, ball):
    frame.fill((0, 0, 0)) # black background

    # render paddles
    paddles[0].render(frame)
    paddles[1].render(frame)

    # render ball
    ball.render(frame)

    pygame.display.update()

def main():
    running = True

    # framerate controller
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        # Draw to frame 
        draw(FRAME, (left_paddle, right_paddle), play_ball)

        # Detect keys pressed and do something
        pressed_keys = pygame.key.get_pressed()
        handle_key_pressed(pressed_keys, left_paddle, right_paddle, FRAME_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

if __name__ == "__main__":
    main()
