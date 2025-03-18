import math
import pygame
import utils
from entities.entity import Entity

class Segment:
    def __init__(self, player, x, y):
        self.player = player

        print(len(self.player.segments))
        self.index = len(self.player.segments) + 1

        self.position = [x,y]
        self.size = player.size

    def tick(self, dt):
        pass
        """
        if 0 <= self.index <= len(self.player.positions):
            self.position = self.player.positions[len(self.player.positions) - self.index]# * self.player.segment_distance]
        """

    def draw(self, surface):
        x,y = self.position
        w,h = self.size
    
        #Draw myself
        pygame.draw.rect(
            surface, 
            (0,255,0), 
            pygame.Rect(x,y,w,h)
        )

class Player(Entity):
    def __init__(self, state, x, y, joystick = None):
        super().__init__(state, x, y, 8, 8)

        #The joystick object that this player will use for input. None means keyboard
        self.joystick = joystick

        #length
        self.max_segments = 12
        self.segment_distance = 100

        self.segments = []

        #past positions
        self.positions = []
        
        #keeping track of growing vars
        self.is_growing = False
        self.grow_time = 0.1
        self.grow_time_elapsed = 0
        self.grow_speed = 192 #Per pxiel
        self.grow_count = 0

        #not growing
        self.speed = 128 #Per second

    def start_growing(self):
        if self.grow_count <= 0:
            self.is_growing = True
            self.segments.append(Segment(self, self.position[0], self.position[1]))

    def stop_growing(self):
        self.is_growing = False
        self.grow_count += 1

        self.segments = []

    def handle_event(self, event):
        #keyboard
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            if event.key == pygame.K_SPACE:
                if event.type == pygame.KEYDOWN:
                    self.start_growing()
                else:
                    self.stop_growing()


        #controller
        if event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
            if self.joystick and event.instance_id == self.joystick.get_instance_id():
                if event.button == pygame.CONTROLLER_BUTTON_A:
                    if event.type == pygame.JOYBUTTONDOWN:
                        self.start_growing()
                    else:
                        self.stop_growing()

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

            #move
            for i in range(2): self.velocity[i] = move[i] * self.speed * dt

            #spawn a new segment when you go too far
            #theirs minus ours
            dist = math.hypot(self.segments[-1].position[0] - self.position[0], self.segments[-1].position[1] - self.position[1])
            if dist >= self.size[0]: #probably replace size with radius 
                self.segments.append(Segment(self, self.position[0], self.position[1]))

            for segment in self.segments: segment.tick(dt)
            
            if len(self.segments) >= self.max_segments:
                self.is_growing = False

                self.grow_time_elapsed = 0
                self.segments = []
        
        #regular platformer
        else:
            self.velocity[0] = move[0] * self.speed * dt

        #handle collisions
        self.handle_collisions(self.state.tiles)

        #reset grow_counter... So player can grow again!
        if self.collision[1] > 0: 
            self.grow_count = 0

        #add position to positions for our segments to follow
        if len(self.positions) > 0 and self.positions[-1] != self.position:
            if len(self.positions) <= self.max_segments * self.segment_distance:
                self.positions.append(self.position)

            #remove first element if it gets too long
            if len(self.positions) > self.max_segments * self.segment_distance:
                self.positions.pop(0)

        print(self.positions)

    def draw(self, surface):
        x,y = self.position
        w,h = self.size

        for segment in self.segments:
            segment.draw(surface)
    
        #Draw myself
        pygame.draw.rect(
            surface, 
            (255,0,0), 
            pygame.Rect(x,y,w,h)
        )
        