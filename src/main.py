import pygame
import utils

from states.playstate import PlayState

class Game:
    def __init__(self, init_state = 'PlayState'):
        self.done = False

        #State variables
        self.states = {'PlayState': PlayState(),}
        self.state_name = init_state
        self.state = self.states[init_state]

        #Initialize pygame!
        pygame.init()

        #Create the clock to keep track of time
        self.clock = pygame.time.Clock()
        
        #Surfaces
        self.screen = pygame.display.set_mode(utils.get_window_size(), pygame.DOUBLEBUF)
        self.surface = pygame.Surface(utils.SURFACE_SIZE)

        #Start state, and begin the main loop!
        self.begin()

    def set_state(self):
        #Set new state, pass persistent data
        
        next_state = self.state.next_state
        persistent_data = self.state.persistent_data

        if next_state in self.states.keys():
            self.state = self.states[next_state]
            self.state_name = next_state

        self.state.start(persistent_data)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            self.state.handle_event(event)
    
    def tick(self, dt):
        if self.state.done: 
            self.set_state()
            
        self.state.tick(dt)

    def draw(self, screen):
        self.state.draw(self.surface)
        
        scaled_surface = pygame.transform.scale(
            self.surface, 
            utils.get_window_size()
        )
        
        screen.blit(scaled_surface, (0, 0))

    def begin(self):
        self.state.start({})
        
        while not self.done:
            dt = self.clock.tick(utils.FRAME_RATE) / 1000

            self.handle_events()
            self.tick(dt)
            self.draw(self.screen)

            pygame.display.flip()

Game()