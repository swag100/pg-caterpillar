import pygame

#window
SURFACE_SIZE = (240, 180)
SURFACE_ZOOM = 2

FRAME_RATE = 60

#game
GRAVITY = 16

def get_window_size():
    return tuple(x * SURFACE_ZOOM for x in SURFACE_SIZE)

def get_joysticks():
    return [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]