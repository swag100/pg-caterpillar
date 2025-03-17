import math
import pygame
import utils
from entities.entity import Entity

class Player(Entity):
    def __init__(self, state, x, y, joystick = None):
        super().__init__(state, x, y, 8, 8)

        #The joystick object that this player will use for input. None means keyboard
        self.joystick = joystick

        self.max_length = 12
        
        self.is_growing = False
        self.grow_time = 0.6
        self.grow_time_elapsed = 0

        self.speed = 256 #Per second
        
        self.segments = []

    def handle_event(self, event):
        #keyboard
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            if event.key == pygame.K_SPACE:
                self.is_growing = event.type == pygame.KEYDOWN

        #controller
        if event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
            if self.joystick and event.instance_id == self.joystick.get_instance_id():
                if event.button == pygame.CONTROLLER_BUTTON_A:
                    self.is_growing = event.type == pygame.JOYBUTTONDOWN

        #do pause logic

    def tick(self, dt):
        #apply gravity
        self.velocity[1] += utils.GRAVITY * dt

        #nullify gravity if you're growing longer
        if self.is_growing:
            self.velocity[1] = 0
        
        #movement
        if self.joystick:
            move = [self.joystick.get_axis(0), self.joystick.get_axis(1)]

            #apply deadzone
            for i in range(2):
                if abs(move[i]) <= 0.2:
                    move[i] = 0
        else:
            keys = pygame.key.get_pressed()

            move = [keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w]]

            #normalize this vector
            magnitude = math.sqrt(move[0] ** 2 + move[1] ** 2)

            if magnitude != 0:
                move = [x / magnitude for x in move]

        #apply move    
        self.velocity[0] = move[0] * self.speed * dt
        if self.is_growing:
            self.velocity[1] = move[1] * self.speed * dt

        #handle collisions
        self.handle_collisions(self.state.tiles)

    def draw(self, surface):
        x,y = self.position
        w,h = self.size
    
        #Draw myself
        pygame.draw.rect(
            surface, 
            (255,0,0), 
            pygame.Rect(x,y,w,h)
        )
        