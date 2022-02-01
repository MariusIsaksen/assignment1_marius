#!/usr/bin/env python3

import pygame
from pygame.locals import * 

from pygame import Vector2
import pygame

SCREEN_X = 640
SCREEN_Y = 640

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
pygame.display.set_caption("Breakoutgame")

#defining background, block and paddle colors
background = (0, 0, 0)

block_red = (255, 80, 90)
block_green = (80, 170, 80)
block_blue = (70, 170, 230)

paddle_col = (140, 130, 150)
paddle_outline = (255, 255, 255)

#defining game variables
colomns = 6
rows = 6
clock = pygame.time.Clock()
fps = 60

def intersect_rectangle_circle(rec_pos, sx, sy,
                               circle_pos, circle_radius, circle_speed):
    """ Determine if a rectangle and a circle intersects.
    Only works for a rectangle aligned with the axes.
    Parameters:
    rec_pos     - A Vector2 representing the position of the rectangles upper,
                  left corner.
    sx          - Width of rectangle.
    sy          - Height of rectangle.
    circle_pos  - A Vector2 representing the circle's position.
    circle_radius - The circle's radius.
    circle_speed - A Vector2 representing the circles speed.
    Returns:
    None if no intersection. 
    If the rectangle and the circle intersect,returns a 
    normalized Vector2 pointing in the direction the circle will
    move after the collision.
    """

    # Position of the walls relative to the ball
    top = (rec_pos.y) - circle_pos.y
    bottom = (rec_pos.y + sy) - circle_pos.y
    left = (rec_pos.x) - circle_pos.x
    right = (rec_pos.x + sx) - circle_pos.x

    r = circle_radius
    intersecting = left <= r and top <= r and right >= -r and bottom >= -r

    if intersecting:
        # Now need to figure out the vector to return.
        impulse = circle_speed

        if abs(left) <= r and impulse.x > 0:
            impulse.x = -impulse.x
        if abs(right) <= r and impulse.x < 0:
            impulse.x = -impulse.x
        if abs(top) <= r and impulse.y > 0:
            impulse.y = -impulse.y
        if abs(bottom) <= r and impulse.y < 0:
            impulse.y = -impulse.y
        return impulse
    return None

#rectangle block class
class rectangle():
    def __init__(self):
        self.width = SCREEN_X // colomns
        self.height = 50

    def create_rectangle(self):
        self.blocks = []
        #define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            #reset the block row list
            block_row = []
            #iterating through each column in that row
            for colomn in range(colomns):
                #generate x and y positions for each block and create a rectangle from that
                block_x = (colomn * self.width)
                block_y = (row * self.height)
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                #assign block strength based on row
                if row < 2: 
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                #create a list at this point to store the rect and colour data 
                block_individual = [rect, strength]
                #append that individual block to the block row
                block_row.append(block_individual)
            #append the row to the full list of blocks
            self.blocks.append(block_row)
            
    def draw_rectangle(self):
        for row in self.blocks:
            for block in row:
                #assign a colour based on block strength
                if block[1] == 3:
                    block_color = block_blue
                elif block[1] == 2:
                    block_color = block_green
                elif block[1] == 1:
                    block_color = block_red
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, background, (block[0]), 2)

#paddle class
class paddle():
    def __init__(self):
        #define paddle variables
        self.height = 20
        self.width = int(SCREEN_X / colomns)
        self.position = Vector2((int((SCREEN_X / 2) - (self.width / 2))), (SCREEN_Y - (self.height * 2)))
        self.speed = 10
        self.rect = Rect(self.position.x, self.position.y, self.width, self.height)
        self.direction = 0

    def move(self):
        #reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_X:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 2)

#ball class
class circle(): 
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10
        self.position_ball = Vector2(300, 400)
        self.rect = Rect(self.position_ball.x, self.position_ball.y, self.radius * 2, self.radius * 2)
        self.speed = Vector2(4, -4)
        self.game_over = 0 

    def move(self):
    
        #Checking for collision with walls
        if self.rect.left < 0 or self.rect.right > SCREEN_X:
            self.speed.x *= -1


        #checking for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed.y *= -1
        if self.rect.bottom > SCREEN_Y:
            self.game_over = -1


        impulse = intersect_rectangle_circle((player_paddle.rect),
                                             player_paddle.width,
                                             player_paddle.height,
                                             self.position_ball,
                                             self.radius,
                                             (self.speed.x, self.speed.y))
        if impulse:
            draw_vec_from_ball(impulse, (0, 255, 255))
            print("Hit")
        
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius, 2)


#create a rectangle
rectangle = rectangle()
rectangle.create_rectangle()

#create paddle
player_paddle = paddle()

#create ball
ball = circle(player_paddle.position.x + (player_paddle.width // 2), player_paddle.position.y - player_paddle.height)

pygame.init()            
while True:

    clock.tick(fps)
    screen.fill(background)

    #draw wall
    rectangle.draw_rectangle()

    #draw paddle
    player_paddle.draw()
    player_paddle.move()

    #draw ball 
    ball.draw()
    ball.move()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    
    # print(event)


print("Ferdig") 