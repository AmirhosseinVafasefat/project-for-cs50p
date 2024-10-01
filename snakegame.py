import sys, random, pygame

pygame.init()

WINSIZE = WINW, WINH = 750, 750
WIN = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Snake Game")

FPS = 5
WHITE = 255, 255, 255
BLACK = 0, 0, 0

TILE_SIZE = 50
START = 350
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
    
    def movement(self):
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y

        if self.rotation == 0 and self.head.x + TILE_SIZE * 2 <= WINW:
            self.head.x += TILE_SIZE
        elif self.rotation == 90 and self.head.y - TILE_SIZE >= 0:
            self.head.y -= TILE_SIZE
        elif self.rotation == 180 and self.head.x - TILE_SIZE >= 0:
            self.head.x -= TILE_SIZE
        elif self.rotation == 270 and self.head.y + TILE_SIZE * 2 <= WINH:
            self.head.y += TILE_SIZE

        self.body.remove(self.head)

    
class Apple():
    def __init__(self) -> None:
        self.x = int(random.randint(0, WINH)/TILE_SIZE)*TILE_SIZE
        self.y = int(random.randint(0, WINH)/TILE_SIZE)*TILE_SIZE

def main():
    snake = Snake()
    apple = Apple()
    score = 0
    inputRotation = 90

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(score)
                pygame.quit()
                sys.exit()
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

        snake.movement()

        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(snake.body[len(snake.body)-1].x, snake.body[len(snake.body)-1].y, TILE_SIZE, TILE_SIZE))
            apple = Apple()
            score += 1

        WIN.fill(WHITE)
        for i in range(0, WINW, TILE_SIZE):
            pygame.draw.line(WIN, BLACK, (i, 0), (i, WINH))
            pygame.draw.line(WIN, BLACK, (0, i), (WINW, i))
        rotated_head = pygame.transform.rotate(HEAD_IMAGE, snake.rotation)
        
        for part in snake.body:
            WIN.blit(BODY_IMAGE, (part.x, part.y))
        WIN.blit(APPLE_IMAGE, (apple.x, apple.y))
        WIN.blit(rotated_head, (snake.head.x, snake.head.y))
        pygame.display.update()

if __name__ == "__main__":
    main()