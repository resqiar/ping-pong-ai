import pygame

def handle_key_pressed(keys, left_paddle, right_paddle, frame_height):
    if keys[pygame.K_w]:
        left_paddle.move("up")
    if keys[pygame.K_s]:
        left_paddle.move("down")
    if keys[pygame.K_UP]:
        right_paddle.move("up")
    if keys[pygame.K_DOWN]:
        right_paddle.move("down")

    # clamp the paddle
    # meaning that if it go out of bound, clamp to max frame_height
    left_paddle.clamp(frame_height)
    right_paddle.clamp(frame_height)
