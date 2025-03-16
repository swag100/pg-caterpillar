import pygame
from states.state import State

#Import necessary objects
from entities.player import Player

class PlayState(State):
    def start(self, persistent_data): 
        super().__init__()
        self.persistent_data = persistent_data
        
        self.tiles = [
            pygame.Rect(0,100,100,20),
            pygame.Rect(150,100,100,20)
        ]
        self.entities = [
            Player(self,0,0)
        ]
		
    def handle_event(self, event):
        for entity in self.entities: entity.handle_event(event)

    def tick(self, dt):
        for entity in self.entities: entity.tick(dt)

    def draw(self, surface):
        surface.fill((255,255,255))
        
        for tile in self.tiles: 
            pygame.draw.rect(surface, (128,128,128), tile)
        
        for entity in self.entities: 
            entity.draw(surface)