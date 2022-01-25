#!/usr/bin/env python3

import pygame
from pygame.locals import * 
import random


SCREEN_X = 640
SCREEN_Y = 480

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
pygame.display.set_caption("Breakout")

#define background and block colors
background = (0, 0, 0)

block_red = (255, 80, 90)
block_green = (80, 170, 80)
block_blue = (70, 170, 230)

colomns = 6
rows = 6


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
                block_x = colomn * self.width
                block_y = row * self.height
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
                #append that individual vlock to the block row
                block_row.append(block_individual)
        #append the row to the full list of blocks
        self.blocks.append(block_row)

    

    def draw_rectangle(self):
        for row in self.blocks:
            for block in row:
                #assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, background, (block[0]), 2)

#create a rectangle
rectangle = rectangle()
rectangle.create_rectangle()
            
while True:

    screen.fill(background)

    #draw wall
    rectangle.draw_rectangle()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()
    
    # print(event)


print("Ferdig") 