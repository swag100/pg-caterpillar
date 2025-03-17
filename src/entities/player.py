import pygame
import utils
from entities.entity import Entity

class Player(Entity):
    """A segment that takes user input and manages other segments"""
    def __init__(self, state, x, y, joy = None):
        super().__init__(state, x, y, 8, 8)

        #the controlling method of this player - None means keyboard.
        self.joy = joy

        self.max_length = 12
        
        self.is_growing = False
        self.grow_time = 0.6
        self.grow_time_elapsed = 0
        
        self.segments = []

    def handle_key_event(self, event):
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            if event.key == pygame.K_SPACE:
                self.is_growing = event.type == pygame.KEYDOWN

    def handle_joy_event(self, event):
        #controller
        if event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
            if event.joy == self.joy:
                if event.button == pygame.CONTROLLER_BUTTON_A:
                    self.is_growing = event.type == pygame.JOYBUTTONDOWN

        if event.type == pygame.JOYAXISMOTION:
            if event.joy == self.joy:
                #Exclude triggers, apply deadzone
                if event.axis < 2 and abs(event.value) >= 0.1:
                    print(event.axis % 2, event.value)
    
    def handle_event(self, event):
        if self.joy != None: #controller controlled character
            self.handle_joy_event(event)
        else:
            self.handle_key_event(event)

        #do pause logic

    def tick(self, dt):
        #apply gravity
        self.velocity[1] += utils.GRAVITY * dt

        #nullify gravity if you're growing longer
        if self.is_growing:
            self.velocity[1] = 0
        
        #movement
        keys = pygame.key.get_pressed()

        move = [
            (keys[pygame.K_d]-keys[pygame.K_a])*64*dt,
            (keys[pygame.K_s]-keys[pygame.K_w])*64*dt
        ]
        
        self.velocity[0] = move[0]
        if self.is_growing:
            self.velocity[1] = move[1]

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
        