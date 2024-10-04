import random, pygame

pygame.init()

WINSIZE = WINW, WINH = 750, 750
WIN = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Snake Game")

FPS = 2

WHITE = 255, 255, 255
BLACK = 0, 0, 0

TILE_SIZE = 50
START = 350
RTURN_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/rightturn.png"), (TILE_SIZE, TILE_SIZE)), -90)
LTURN_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/leftturn.png"), (TILE_SIZE, TILE_SIZE)), -90)
TAIL_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/tail.png"), (TILE_SIZE, TILE_SIZE)), -90)
DEAD_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/dead.png"), (TILE_SIZE, TILE_SIZE)), -90)
HEAD_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/head.png"), (TILE_SIZE, TILE_SIZE)), -90)
BODY_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/body.png"), (TILE_SIZE, TILE_SIZE)), -90)
BOX_IMAGE = pygame.transform.scale(pygame.image.load("assets/box.png"), (TILE_SIZE, TILE_SIZE))
APPLE_IMAGE = pygame.transform.scale(pygame.image.load("assets/apple.png"), (TILE_SIZE, TILE_SIZE))

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
        snake.head.x += TILE_SIZE
    elif snake.rotation == 90:
        snake.head.y -= TILE_SIZE
    elif snake.rotation == 180:
        snake.head.x -= TILE_SIZE
    elif snake.rotation == 270:
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

def is_dead(snake):
    if snake.head.x + TILE_SIZE >= WINW or snake.head.y  <= 0 or snake.head.x <= 0 or snake.head.y + TILE_SIZE >= WINH:
        return True
    for part in snake.body:
        if snake.head.x == part.x and snake.head.y == part.y:
            return True

def draw_windows(snake, apple, tail_dir):
    WIN.fill(WHITE)
    for i in range(0, WINW, TILE_SIZE):
        pygame.draw.line(WIN, BLACK, (i, 0), (i, WINH))
        WIN.blit(BOX_IMAGE, (i, 0))
        WIN.blit(BOX_IMAGE, (i, WINH-TILE_SIZE))
        
    for i in range(0, WINH, TILE_SIZE):
        pygame.draw.line(WIN, BLACK, (0, i), (WINW, i))
        WIN.blit(BOX_IMAGE, (0, i))
        WIN.blit(BOX_IMAGE, (WINW-TILE_SIZE, i))
        
    if snake.dead:
        rotated_head = pygame.transform.rotate(DEAD_IMAGE, snake.rotation)
    else:
        rotated_head = pygame.transform.rotate(HEAD_IMAGE, snake.rotation)
    
    snake.body.append(snake.head)
    for i, part in enumerate(snake.body):
        if not i == 0 and not i == len(snake.body)- 1:
            if snake.body[i-1].x == snake.body[i].x == snake.body[i+1].x:
                WIN.blit(pygame.transform.rotate(BODY_IMAGE, 90), (part.x, part.y))
            elif snake.body[i-1].y == snake.body[i].y == snake.body[i+1].y:
                WIN.blit(BODY_IMAGE, (part.x, part.y))

            elif snake.body[i-1].x == snake.body[i].x and snake.body[i-1].y < snake.body[i].y :
                if snake.body[i].x < snake.body[i+1].x:
                    WIN.blit(pygame.transform.rotate(LTURN_IMAGE, 270), (part.x, part.y))
                elif snake.body[i].x > snake.body[i+1].x:
                    WIN.blit(pygame.transform.rotate(RTURN_IMAGE, 270), (part.x, part.y))

            elif snake.body[i-1].x == snake.body[i].x and snake.body[i-1].y > snake.body[i].y :
                if snake.body[i].x < snake.body[i+1].x:
                    WIN.blit(pygame.transform.rotate(RTURN_IMAGE, 90), (part.x, part.y))
                elif snake.body[i].x > snake.body[i+1].x:
                    WIN.blit(pygame.transform.rotate(LTURN_IMAGE, 90), (part.x, part.y))
            
            elif snake.body[i-1].y == snake.body[i].y and snake.body[i-1].x > snake.body[i].x :
                if snake.body[i].y < snake.body[i+1].y:
                    WIN.blit(pygame.transform.rotate(LTURN_IMAGE, 180), (part.x, part.y))
                elif snake.body[i].y > snake.body[i+1].y:
                    WIN.blit(pygame.transform.rotate(RTURN_IMAGE, 180), (part.x, part.y))

            elif snake.body[i-1].y == snake.body[i].y and snake.body[i-1].x < snake.body[i].x :
                if snake.body[i].y < snake.body[i+1].y:
                    WIN.blit(RTURN_IMAGE, (part.x, part.y))
                elif snake.body[i].y > snake.body[i+1].y:
                    WIN.blit(LTURN_IMAGE, (part.x, part.y))

    if snake.body[0].y == snake.body[1].y and snake.body[0].x < snake.body[1].x:
        tail_dir = 0
    elif snake.body[0].y == snake.body[1].y and snake.body[0].x > snake.body[1].x:
        tail_dir = 180
    elif snake.body[0].x == snake.body[1].x and snake.body[0].y < snake.body[1].y:
        tail_dir = 270
    elif snake.body[0].x == snake.body[1].x and snake.body[0].y > snake.body[1].y:
        tail_dir = 90

    snake.body.remove(snake.head)
    rotated_tail = pygame.transform.rotate(TAIL_IMAGE, tail_dir)
    WIN.blit(APPLE_IMAGE, (apple.x, apple.y))
    WIN.blit(rotated_head, (snake.head.x, snake.head.y))
    WIN.blit(rotated_tail, (snake.body[0].x, snake.body[0].y))
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
    tail_dir = 90
    apple = Apple()
    score = 0

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        event_handler(snake)

        movement(snake)

        if is_dead(snake):
            run = False
            snake.dead = True

        draw_windows(snake, apple, tail_dir)

        if can_eat_apple(snake, apple):
            apple = Apple()
            print(f"{apple.x}, {apple.y}")
            while not correct_apple_position(apple, snake):
                apple = Apple()
                print(f"re-evaluate. {apple.x}, {apple.y}")
            score += 1

    game_over()

if __name__ == "__main__":
    main()