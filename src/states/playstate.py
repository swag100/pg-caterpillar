import pygame
import utils
from states.state import State

#Import necessary objects
from entities.player import Player

#Init joysticks!
pygame.joystick.init()

class PlayState(State):
    def start(self, persistent_data): 
        super().__init__()
        self.persistent_data = persistent_data
        
        self.tiles = [
            pygame.Rect(0,100,100,20),
            pygame.Rect(150,100,100,20)
        ]
        self.entities = []

        self.joysticks = utils.get_joysticks()
		
    def handle_event(self, event):
        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED, pygame.JOYBUTTONDOWN]:
            self.joysticks = utils.get_joysticks()

            #update players
            for joy in range(len(self.joysticks)):
                #check if we dont need to make a new player for a joystick
                player_already_exists = False
                for entity in self.entities:
                    if hasattr(entity, 'joy'):
                        if entity.joy == joy:
                            player_already_exists = True

                        #check for who needs to be removed
                        if entity.joy not in range(len(self.joysticks)):
                            self.entities.remove(entity)

                if not player_already_exists:
                    self.entities.append(Player(self, 0, 0, joy))

        for entity in self.entities: entity.handle_event(event)

    def tick(self, dt):
        for entity in self.entities: entity.tick(dt)

    def draw(self, surface):
        surface.fill((255,255,255))
        
        for tile in self.tiles: 
            pygame.draw.rect(surface, (128,128,128), tile)
        
        for entity in self.entities: 
            entity.draw(surface)