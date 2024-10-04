import random, pygame

pygame.init()

WINSIZE = WINW, WINH = 750, 750
WIN = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Snake Game")

FPS = 5

WHITE = 255, 255, 255
BLACK = 0, 0, 0

TILE_SIZE = 50
START = 350
DEAD_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/deadgreenhead.png"), (TILE_SIZE, TILE_SIZE)), -90)
HEAD_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/greenhead.png"), (TILE_SIZE, TILE_SIZE)), -90)
BODY_IMAGE = pygame.transform.scale(pygame.image.load("assets/greenblock.png"), (TILE_SIZE, TILE_SIZE))
APPLE_IMAGE = pygame.transform.scale(pygame.image.load("assets/redblock.png"), (TILE_SIZE, TILE_SIZE))

class Snake():
    def __init__(self) -> None:
        self.x = START
        self.y = START
        self.rotation = 90
        self.head = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self.body = [pygame.Rect(self.x, self.y - TILE_SIZE, TILE_SIZE, TILE_SIZE)]
        self.dead = False
    
class Apple():
    def __init__(self) -> None:
        self.x = int(random.randint(0 + TILE_SIZE, WINW - TILE_SIZE)/TILE_SIZE)*TILE_SIZE
        self.y = int(random.randint(0 + TILE_SIZE, WINH - TILE_SIZE)/TILE_SIZE)*TILE_SIZE

def correct_apple_position(apple, snake):
    snake.body.append(snake.head)
    for part in snake.body:
        if apple.x == part.x and apple.y == part.y:
            snake.body.remove(snake.head)
            return False
    else:
        snake.body.remove(snake.head)
        return True
    
def event_handler(snake):
    inputRotation = snake.rotation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                inputRotation = 0
            elif event.key == pygame.K_UP:
                inputRotation = 90
            elif event.key == pygame.K_LEFT:
                inputRotation = 180
            elif event.key == pygame.K_DOWN:
                inputRotation = 270

    if (snake.rotation in (0, 180) and inputRotation in (90, 270)) or (snake.rotation in (90, 270) and inputRotation in (0, 180)):
        snake.rotation = inputRotation

def movement(snake):
    snake.body.append(snake.head)
    for i in range(len(snake.body)-1):
        snake.body[i].x, snake.body[i].y = snake.body[i+1].x, snake.body[i+1].y

    if snake.rotation == 0:
        if snake.head.x + TILE_SIZE * 2>= WINW:
            snake.dead = True
        snake.head.x += TILE_SIZE
    elif snake.rotation == 90:
        if snake.head.y - TILE_SIZE <= 0:
            snake.dead = True
        snake.head.y -= TILE_SIZE
    elif snake.rotation == 180:
        if snake.head.x - TILE_SIZE <= 0:
            snake.dead = True
        snake.head.x -= TILE_SIZE
    elif snake.rotation == 270:
        if snake.head.y + TILE_SIZE * 2 >= WINH:
            snake.dead = True
        snake.head.y += TILE_SIZE

    snake.body.remove(snake.head)

def can_eat_apple(snake, apple):
    if snake.head.x == apple.x and snake.head.y == apple.y:  
        snake.body.reverse()
        snake.body.append(pygame.Rect(snake.body[len(snake.body)-1].x, snake.body[len(snake.body)-1].y, TILE_SIZE, TILE_SIZE))
        snake.body.reverse()
        return True
    else:
        return False

def draw_windows(snake, apple):
    WIN.fill(WHITE)
    for i in range(0, WINW, TILE_SIZE):
        pygame.draw.line(WIN, BLACK, (i, 0), (i, WINH))
        pygame.draw.rect(WIN, BLACK, (i, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(WIN, BLACK, (i, WINH-TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
    for i in range(0, WINH, TILE_SIZE):
        pygame.draw.line(WIN, BLACK, (0, i), (WINW, i))
        pygame.draw.rect(WIN, BLACK, (0, i, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(WIN, BLACK, (WINW-TILE_SIZE, i, TILE_SIZE, TILE_SIZE))
        
    if snake.dead:
        rotated_head = pygame.transform.rotate(DEAD_IMAGE, snake.rotation)
    else:
        rotated_head = pygame.transform.rotate(HEAD_IMAGE, snake.rotation)
    for part in snake.body:
        WIN.blit(BODY_IMAGE, (part.x, part.y))
    WIN.blit(APPLE_IMAGE, (apple.x, apple.y))
    WIN.blit(rotated_head, (snake.head.x, snake.head.y))
    pygame.display.update()

def game_over():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('GAME OVER', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (WINW // 2, WINH // 2)
    WIN.blit(text, textRect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def main():
    snake = Snake()
    apple = Apple()
    score = 0

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        event_handler(snake)

        movement(snake)

        if can_eat_apple(snake, apple):
            apple = Apple()
            print(f"{apple.x}, {apple.y}")
            while not correct_apple_position(apple, snake):
                apple = Apple()
                print(f"re-evaluate. {apple.x}, {apple.y}")
            score += 1
        
        if snake.dead:
            run = False

        draw_windows(snake, apple)

    game_over()

if __name__ == "__main__":
    main()