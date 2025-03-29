import pygame 
import random

# pygame setup
pygame.init()

width = 512
height = 512

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

def xor(bool1, bool2):
    return (bool1 and not bool2) or (not bool1 and bool2)

#draw rectangles with screen wrapping functionality
def draw_rect(pos, size, colour):
    rtangle = pygame.Rect(pos, size)
    pygame.draw.rect(screen, colour, rtangle)

#draw a panel out of basic shapes (with wrapping)
def draw_panel(pos, size, colour):
    rtangle = pygame.Rect(pos, size)

    #check these for errors
    top_size = (size[0]-5, size[1]-5) 
    top_colour = (colour[0]-15, colour[0]-15, colour[0]-15)

    rtangle_top = pygame.Rect(pos, top_size)
    pygame.draw.rect(screen, colour, rtangle)
    pygame.draw.rect(screen, top_colour, rtangle_top)

    bolt_size = 3
    bolt_offset = 7
    #draw bolt details
    pygame.draw.circle(screen, (150,150,150), (pos[0] + bolt_offset, pos[1] + bolt_offset), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + (top_size[0] - bolt_offset), pos[1] + bolt_offset), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + bolt_offset, pos[1] + (top_size[1] - bolt_offset)), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + (top_size[0] - bolt_offset), pos[1] + (top_size[1] - bolt_offset)), bolt_size)


#will draw shapes wrapped
def wrap_draw(to_draw, pos, size, dimensions, colour):
    offset_X = pos[0]
    offset_Y = pos[1]

    redraw_X = False
    redraw_Y = False

    if (pos[0] + size[0]) > dimensions[0]:
        offset_X = (pos[0] - dimensions[0])
        redraw_X = True

    if (pos[1] + size[1]) > dimensions[1]:
        offset_Y = (pos[1] - dimensions[1])
        redraw_Y = True

    #redraw on all axes
    if redraw_X and redraw_Y:
        print("Redraw all axes")
        to_draw((pos[0], offset_Y), size, colour)
        to_draw((offset_X, pos[1]), size, colour)
        to_draw((offset_X, offset_Y), size, colour)

    #redraw on X or Y
    if xor(redraw_X, redraw_Y):
        print("Redraw X-Y axes")
        to_draw((offset_X, offset_Y), size, colour)

while running:
    #poll events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #fill screen with black to clear
    screen.fill("black")

    for i in range(1000):
        random_col = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        random_pos = (random.randrange(0,width), random.randrange(0,height))
        
        random_width = random.randrange(50,250)
        random_height = random.randrange(20, 75)
        darkness = random.randrange(50, 150)
        random_col = (darkness,darkness,darkness)

        #draw_rect(random_pos, (random_width,random_height), random_col)
        #wrap_draw(draw_rect, random_pos, (random_width, random_height), (width,height), random_col)

        draw_panel(random_pos, (random_width,random_height), random_col)
        wrap_draw(draw_panel, random_pos, (random_width, random_height), (width,height), random_col)

    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.image.save(screen, "screenshot.png")

    #regenerate new image ever 2 seconds
    dt = clock.tick(0.5) / 1000

pygame.quit()