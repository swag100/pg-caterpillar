import pygame
from entities.entity import Entity

class Player(Entity):
    """A segment that takes user input and manages other segments"""
    def __init__(self, state, x, y):
        super().__init__(state, x, y, 8, 8)
        
        self.states = ["idle", "crawl", "grow"]
        self.state = "idle"
        
        self.length = 1
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.collided[1]:
                    self.velocity[1] -= 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.velocity[1] < -2:
                    self.velocity[1] = -2

    def tick(self, dt):
        super().tick(dt)
        
        keys = pygame.key.get_pressed()
        
        self.xmove = (keys[pygame.K_d]-keys[pygame.K_a])*64*dt
        
        self.velocity[0] = self.xmove
        #self.velocity[1] = (keys[pygame.K_s]-keys[pygame.K_w])*64*dt

    def draw(self, surface):
        x,y = self.position
        w,h = self.size
    
        #draw my tail
        for i in range(self.length):
            pygame.draw.rect(
                surface, 
                ((i*16)%255,0,0), 
                pygame.Rect(x-(self.xmove*i),y,w,h)
            )
        
            
    
        #Draw myself
        pygame.draw.rect(
            surface, 
            (255,0,0), 
            pygame.Rect(x,y,w,h)
        )
        