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
        self.players = []

        self.joysticks = utils.get_joysticks()
        for joystick in self.joysticks:
            for player in self.players:
                if player.joystick == joystick:
                    #Do not run rest of code IF theres already a player assigned to this joystick
                    continue

            self.players.append(
                Player(self, 16, 16, joystick)
            )
		
    def handle_event(self, event):
        for entity in self.players: entity.handle_event(event)

    def tick(self, dt):
        for entity in self.players: entity.tick(dt)

    def draw(self, surface):
        surface.fill((255,255,255))
        
        for tile in self.tiles: 
            pygame.draw.rect(surface, (128,128,128), tile)
        
        for entity in self.players: 
            entity.draw(surface)