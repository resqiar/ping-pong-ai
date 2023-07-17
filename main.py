import pygame
from paddle import Paddle
from ball import Ball
from handle_key_pressed import handle_key_pressed
from handle_collision import handle_collision

# init game
pygame.init()

FRAME_WIDTH, FRAME_HEIGHT = 700, 500
FPS = 60

FRAME = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
pygame.display.set_caption("Ping Pong AI")

# Scores Font
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

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

def draw(frame, paddles, ball, left_score, right_score):
    frame.fill((0, 0, 0)) # black background

    # Draw scores
    left_score_txt = SCORE_FONT.render(str(left_score), True, (255, 255, 255))
    right_score_txt = SCORE_FONT.render(str(right_score), True, (255, 255, 255))

    frame.blit(left_score_txt, (FRAME_WIDTH // 4 - left_score_txt.get_width() // 2, 20))
    frame.blit(right_score_txt, (FRAME_WIDTH * (3 / 4) - right_score_txt.get_width() // 2, 20))

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

    # Scores
    right_score = 0
    left_score = 0

    while running:
        clock.tick(FPS)

        # Draw to frame 
        draw(FRAME, (left_paddle, right_paddle), play_ball, left_score, right_score)

        # Detect keys pressed and do something
        pressed_keys = pygame.key.get_pressed()
        handle_key_pressed(pressed_keys, left_paddle, right_paddle, FRAME_HEIGHT)

        # move the ball 
        play_ball.move()

        # handle ball collisions
        handle_collision(play_ball, left_paddle, right_paddle, FRAME_HEIGHT)

        # calculate if someone win
        if play_ball.x < 0:
            right_score += 1
        elif play_ball.x > FRAME_WIDTH:
            left_score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

if __name__ == "__main__":
    main()
