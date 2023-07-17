def handle_collision(ball, left_paddle, right_paddle, frame_height):
    # ceiling / wall collisions
    # pretty easy, we just need to change the direction
    # of the incoming ball, lets say when ball hit 
    # with -10 then swap the direction to +10
    if ball.y + ball.radius >= frame_height or ball.y - ball.radius <= 0:
        ball.v_y *= -1

    # check if ball is moving leftside (negative value)
    if ball.v_x < 0:
        # if leftside of the ball touching right side of the paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                # reverse x direction
                ball.v_x *= -1

                # make y dynamic direction
                new_y = calculate_paddle_displacement(ball, left_paddle)
                ball.v_y = new_y

    # ball is moving rightside
    else:
        # if rightside of the ball touching left side of the paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                # reverse x direction
                ball.v_x *= -1

                # make y dynamic direction
                ball.v_y = calculate_paddle_displacement(ball, right_paddle)

def calculate_paddle_displacement(ball, paddle):
    paddle_middle_y = paddle.y + paddle.height / 2
    y_diff = paddle_middle_y - ball.y
    reduction_factor = (paddle.height / 2) / ball.MAX_VELOCITY

    return -1 * (y_diff / reduction_factor)
