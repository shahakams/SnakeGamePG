import pygame
from sys import exit
from pygame.math import Vector2
from random import randint

pygame.init()


class FRUIT:
    def __init__(self):
        self.x = randint(0, CELL_NUMBER - 1)
        self.y = randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE,
                                 CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, 'red', fruit_rect)

    def randomize(self):
        self.x = randint(0, CELL_NUMBER - 1)
        self.y = randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, 'green', block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.body.insert(0, self.snake.body[0])

        for block in self.snake.body[1:]:
            if self.fruit.pos == block:
                self.fruit.randomize()

    def check_fail(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= 20:  # Out of bounds X
            self.game_over()

        if self.snake.body[0].y < 0 or self.snake.body[0].y >= 20:  # Out of bounds Y
            self.game_over()

        for block in self.snake.body[2:]:  # Snake collides with itself
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.fruit.randomize()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)  # Snake starts with 3 blocks
        score_surface = GAME_FONT.render(score_text, False, (255, 255, 255))
        score_x = CELL_SIZE * CELL_NUMBER - 60
        score_y = CELL_SIZE * CELL_NUMBER - 60
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)


CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN_WIDTH, SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER
GAME_FONT = pygame.font.Font('Graphics/dogica.ttf', 25)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

background_color = (0, 0, 0)

main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake.direction != Vector2(0, 1):
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_s:
                if main_game.snake.direction != Vector2(0, -1):
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                if main_game.snake.direction != Vector2(1, 0):
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_d:
                if main_game.snake.direction != Vector2(-1, 0):
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill(background_color)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
