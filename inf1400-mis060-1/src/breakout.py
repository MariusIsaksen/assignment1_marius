#!/usr/bin/env python3

import pygame
from pygame.locals import * 

from pygame import Vector2
import pygame

import os

SCREEN_X = 600
SCREEN_Y = 600

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
pygame.display.set_caption("Breakoutgame")

pygame.init()  
pygame.mixer.init()

#defining colors
background = (0, 0, 0)

block_red = (255, 0, 0)
block_green = (0, 128, 0)
block_blue = (0, 0, 255)

paddle_col = (140, 130, 150)
paddle_outline = (255, 255, 255)
ball_col = (215,183,64)

text_col = (130, 120, 150)

#defining game variables
colomns = 5
rows = 6
clock = pygame.time.Clock()
fps = 60
score = 0

#adding background music
background_music = pygame.mixer.music.load(os.path.join('background_music.ogg'))
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)


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

def draw_vec_from_ball(vec, col):
            """ Draw a vector from the mouse controlled circle. """
            pygame.draw.line(screen, col,
                             (ball.position_ball.x, ball.position_ball.y),
                             (ball.position_ball.x + vec.x * 20,
                              ball.position_ball.y + vec.y * 20), 3)

#rectangle block class
class rectangle():
    def __init__(self):
        #defining the rectangle variables
        self.width = SCREEN_X // colomns
        self.height = 40

    def create_rectangle(self):
        #creating a list for the blocks
        self.blocks = []
        for row in range(rows):
            #creating a list for each row of the blocks
            block_row = []
            #going through each column in that row
            for colomn in range(colomns):
                #creating x and y for the blocks
                block_x = (colomn * self.width)
                block_y = (row * self.height)
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                #creating the strength of the blocks depending on which row they are in
                if row < 2: 
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1 
                #creating a list that stores the rectangles and strength of the blocks
                block_individual = [rect, strength]
                #adding the block individuals to the block row list
                block_row.append(block_individual)
            #adding the block row list to the full list of blocks
            self.blocks.append(block_row)

    def draw_rectangle(self):
        for row in self.blocks:
            for block in row:
                #assigning the colours to each of the blockstrengths
                if block[1] == 3:
                    block_color = block_red
                elif block[1] == 2:
                    block_color = block_green
                elif block[1] == 1:
                    block_color = block_blue
                #Drawing the rectangles and outlines.
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, background, (block[0]), 2)
    
    #creating a score implementation
    def score(self):
        font = pygame.font.Font(None, 60)
        text = font.render("Score: " + str(score), 1, text_col)
        screen.blit(text, (240, 400))

#paddle class
class paddle():
    def __init__(self):
        #defining paddle variables
        self.height = 20
        self.width = 100
        self.position = Vector2((int((SCREEN_X / 2) - (self.width / 2))), (SCREEN_Y - (self.height * 2)))
        self.speed = 10
        self.rect = Rect(self.position.x, self.position.y, self.width, self.height)

    def move(self):
        #creating the moving paddle 
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_X:
            self.rect.x += self.speed
            self.direction = 1
    
    def draw(self):
        #Drawing the paddle
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 1)

#ball class
class circle(): 
    def __init__(self, x, y):
        super().__init__()
        #Defining ball variables
        self.radius = 7
        self.position_ball = Vector2(200, 400)
        self.rect = Rect(self.position_ball.x, self.position_ball.y, self.radius * 2, self.radius * 2)
        self.speed = Vector2(4, -4)
        self.game_over = 0
       

    def move(self):
        #Creating collision variable
        collide = 5
        #starting with the wall set as destroyed
        self.rect_destroyed = 1
        row_count = 0
        for row in rectangle.blocks:
            item_count = 0
            for item in row:
                #check for collision
                if self.rect.colliderect(item[0]):
                    #adding 1 to score everytime the ball hits
                    global score
                    score += 1
                    #checking if collision from above, below, left and right
                    if abs(self.rect.bottom - item[0].top) < collide and self.speed.y > 0:
                        self.speed.y *= -1 
                    if abs(self.rect.top - item[0].bottom) < collide and self.speed.y < 0:
                        self.speed.y *= -1 
                    if abs(self.rect.right - item[0].left) < collide and self.speed.x > 0:
                        self.speed.x *= -1 
                    if abs(self.rect.left - item[0].right) < collide and self.speed.x < 0:
                        self.speed.x *= -1 

                    #Reducing the strength of the rectangles when the ball hits
                    if rectangle.blocks[row_count][item_count][1] > 1:
                        rectangle.blocks[row_count][item_count][1] -= 1
                    else:
                        rectangle.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                   
                #Checking if any rectangles left. If there is, sets rect_destroyed to 0 since the game isnt finished
                if rectangle.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    self.rect_destroyed = 0

                item_count += 1

            row_count += 1

        #Checking if wall is destroyed
        if self.rect_destroyed == 1:
            #If the walls are destroyed then game is over and you win.
            self.game_over = 1 

        #Checking for collision with left and right wall
        if self.rect.left < 0 or self.rect.right > SCREEN_X:
            #changing the x speed to -1 so the ball goes the right direction
            self.speed.x *= -1

        #checking for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed.y *= -1
        if self.rect.bottom > SCREEN_Y:
            #if the ball hits the bottom of the screen, set game over to -1
            self.game_over = -1

        #Creating an impulse that activates if the paddle and the ball intersects.
        impulse = intersect_rectangle_circle(paddlebox.rect,
                                             paddlebox.width,
                                             paddlebox.height,
                                             self.rect,
                                             self.radius,
                                             self.speed)
        if impulse:
            impulse = self.speed
           
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

       
     #adding text and music for when the player wins or loses
    def extra(self):
        if self.rect.bottom > SCREEN_Y:
            font = pygame.font.Font('freesansbold.ttf', 60)
            text = font.render('Game Over', True, text_col)
            textRect = text.get_rect ()
            textRect.center = (SCREEN_X // 2, SCREEN_Y // 2)

            sound = pygame.mixer.Sound(os.path.join('game_over_sound_effect.ogg'))
            pygame.mixer.Sound.set_volume(sound, 0.02)
            pygame.mixer.Sound.play(sound)

            pygame.mixer.music.pause()

            screen.fill(background)
            screen.blit(text, textRect)
        
        if self.rect_destroyed == 1:
            
            font = pygame.font.Font('freesansbold.ttf', 40)
            text = font.render('Congratulations, you won!', True, text_col)
            textRect = text.get_rect ()
            textRect.center = (SCREEN_X // 2, SCREEN_Y // 2)

            sound2 = pygame.mixer.Sound(os.path.join('youwon.ogg'))
            pygame.mixer.Sound.set_volume(sound2, 0.07)
            pygame.mixer.Sound.play(sound2)

            pygame.mixer.music.pause()

            screen.fill(background)
            screen.blit(text, textRect)
        
    def draw(self):
        pygame.draw.circle(screen, ball_col, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

#creating rectangle
rectangle = rectangle()
rectangle.create_rectangle()

#creating paddle
paddlebox = paddle()

#creating ball
ball = circle(paddlebox.position.x + (paddlebox.width // 2), paddlebox.position.y - paddlebox.height)

while True:

    clock.tick(fps)
    screen.fill(background)

    #drawing wall
    rectangle.draw_rectangle()
    rectangle.score()

    #drawing paddle
    paddlebox.draw()
    paddlebox.move()

    #drawing ball and extras
    ball.draw()
    ball.move()
    ball.extra()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    
print("Ferdig") 