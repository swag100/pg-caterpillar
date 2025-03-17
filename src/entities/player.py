import pygame
import utils
from entities.entity import Entity

class Player(Entity):
    def __init__(self, state, x, y, joystick = None):
        super().__init__(state, x, y, 8, 8)

        #The joystick object that this player will use for input. None means keyboard
        self.joystick = joystick

        self.default_max_length = 2
        self.max_length = self.default_max_length
        
        self.is_growing = False
        self.grow_time = 0.1
        self.grow_time_elapsed = 0
        self.grow_speed = 8 #Per pxiel

        self.speed = 128 #Per second
        
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
            utils.normalize(move)

        #apply move 
        if self.is_growing:
            if move != [0, 0]:
                self.grow_time_elapsed += dt

            #reset velocity
            self.velocity = [0, 0]

            if self.grow_time_elapsed % self.grow_time <= dt:
                for i in range(2): self.velocity[i] = move[i] * self.grow_speed
            
            if self.grow_time_elapsed >= self.max_length:
                self.is_growing = False
                self.grow_time_elapsed = 0
                self.max_length = 0
        
        #regular platformer
        else:
            self.velocity[0] = move[0] * self.speed * dt

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
        