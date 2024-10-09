import pytest
from project import Apple, Snake, correct_apple_position, move, can_eat_apple

def test_correct_apple_position():
    apple = Apple()
    snake = Snake()
    apple.x = 100
    apple.y = 100
    snake.head.x = 100
    snake.head.y = 100
    assert correct_apple_position(snake, apple) == False

def test_move():
    snake = Snake()
    snake.head.x = 100
    snake.head.y = 100
    snake.headDirection = 90
    move(snake)
    assert snake.head.x == 100 and snake.head.y == 50


def test_can_eat_apple():
    snake = Snake()
    apple = Apple()
    snake.head.x = 100
    snake.head.y = 100
    snake.body[0].x = 150
    snake.body[0].y = 100
    apple.x = 100
    apple.y = 100
    assert can_eat_apple(snake, apple)
    assert snake.body[1].x == 150 and snake.body[1].y == 100