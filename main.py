import pygame 
import random
import inspect

# pygame setup
pygame.init()

width = 512
height = 512

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

def val_in_range(val, min, max):
    if val > max:
        val = max
    elif val < min:
        val = min

    return val

def xor(bool1, bool2):
    return (bool1 and not bool2) or (not bool1 and bool2)

def rect(pos, size, colour):
    rect = pygame.Rect(pos, size)

    col_array = list(colour)
    
    for i, val in enumerate(colour):
        col_array[i] = val_in_range(val, 0, 255)

    colour = tuple(col_array)

    pygame.draw.rect(screen, colour, rect)

def ellipse(pos, size, colour):
    rect = pygame.Rect(pos, size) 

    col_array = list(colour)

    for i, val in enumerate(colour):
        col_array[i] = val_in_range(val, 0, 255)

    colour = tuple(col_array)

    pygame.draw.ellipse(screen, colour, rect)

#draw a panel out of basic shapes
def panel(pos, size, colour, bolt_size=3, bolt_offset=7, top_size=(-1,-1), top_colour=(-1,-1,-1), colour_diff=-15):
    #set defaults
    if bolt_size < 0:
        bolt_size = 3

    #will calculate and set default if user hasn't set any or they're outside spec
    if top_size[0] < 0 or top_size[1] < 0 or size[0] > 5 or size[1] > 5:
        top_size = (size[0]-5, size[1]-5)

    #check if colours in range
    col_array = list(colour)
    top_col_array = list(top_colour)
    
    for i, val in enumerate(colour):
        col_array[i] = val_in_range(val, 0, 255)
        top_col_array[i] = val_in_range((val+colour_diff), 0, 255)

    colour = tuple(col_array)
    top_colour = tuple(top_col_array)

    rect = pygame.Rect(pos, size)
    rect_top = pygame.Rect(pos, top_size)
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, top_colour, rect_top)

    #draw bolt details
    pygame.draw.circle(screen, (150,150,150), (pos[0] + bolt_offset, pos[1] + bolt_offset), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + (top_size[0] - bolt_offset), pos[1] + bolt_offset), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + bolt_offset, pos[1] + (top_size[1] - bolt_offset)), bolt_size)
    pygame.draw.circle(screen, (150,150,150), (pos[0] + (top_size[0] - bolt_offset), pos[1] + (top_size[1] - bolt_offset)), bolt_size)

def pane(pos, size, colour, tri_colour=(-1,-1,-1), colour_diff=15):
    rect = pygame.Rect(pos, size)

    tri_points = (pos, (pos[0] + size[0]-1, pos[1]), (pos[0] ,pos[1] + size[1]-1)) #offset caused by line draw width

    #check if colours in range
    col_array = list(colour)
    tri_col_array = list(tri_colour)
    
    for i, val in enumerate(colour):
        col_array[i] = val_in_range(val, 0, 255)
        tri_col_array[i] = val_in_range((val+colour_diff), 0, 255)

    colour = tuple(col_array)
    tri_colour = tuple(tri_col_array)

    pygame.draw.rect(screen, colour, rect)
    pygame.draw.polygon(screen, tri_colour, tri_points)

#will draw shapes wrapped
def wrap_draw(to_draw, **kwargs):
    sig = inspect.signature(to_draw)
    
    #check for required args
    req_kwargs = {kw: i for kw, i in kwargs.items() if kw in sig.parameters}

    #store for later
    pos_X = req_kwargs["pos"][0] 
    pos_Y = req_kwargs["pos"][1] 
    offset_X = req_kwargs["pos"][0] 
    offset_Y = req_kwargs["pos"][1] 

    redraw_X = False
    redraw_Y = False

    if (req_kwargs["pos"][0] + req_kwargs["size"][0]) > kwargs["dims"][0]:
        offset_X = (req_kwargs["pos"][0] - kwargs["dims"][0])
        redraw_X = True

    if (req_kwargs["pos"][1] + req_kwargs["size"][1]) > kwargs["dims"][1]:
        offset_Y = (req_kwargs["pos"][1] - kwargs["dims"][1])
        redraw_Y = True

    #redraw on all axes
    if redraw_X and redraw_Y:
        #change kwargs for position (required for wrap drawing)
        pos_kwarg = (pos_X, offset_Y)
        req_kwargs["pos"] = pos_kwarg
        to_draw(**req_kwargs)

        pos_kwarg = (offset_X, pos_Y)
        req_kwargs["pos"] = pos_kwarg
        to_draw(**req_kwargs)

        pos_kwarg = (offset_X, offset_Y)
        req_kwargs["pos"] = pos_kwarg
        to_draw(**req_kwargs) 

    if xor(redraw_X, redraw_Y):
        #kwargs pos is offset
        pos_kwarg = (offset_X, offset_Y)
        req_kwargs["pos"] = pos_kwarg
        to_draw(**req_kwargs) 

#draw a shape from given method, with wrapping (initial call plus wrap call)
def draw_shape(to_draw, **kwargs):
    sig = inspect.signature(to_draw)
    
    req_kwargs = {kw: i for kw, i in kwargs.items() if kw in sig.parameters} #required arguments
   
    to_draw(**req_kwargs)
    wrap_draw(to_draw, **req_kwargs, dims=kwargs["dims"]) #takes dims args too

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

        draw_shape(panel, pos=random_pos, size=(random_width,random_height), dims=(width, height), colour=random_col)

    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.image.save(screen, "screenshot.png")

    #regenerate new image ever 2 seconds
    dt = clock.tick(0.5) / 1000

pygame.quit()
