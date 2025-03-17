import utils

class Entity:
    def __init__(self, state, x, y, w, h):
        self.state = state
    
        self.position = [x, y]
        self.size = [w, h]
        
        self.velocity = [0, 0]
        self.collision = [False, False]
    
    def get_collisions(self, tiles):
        collisions = []
        for tile in tiles:
            conditions = [
                self.position[0] < tile.right,
                self.position[0] + self.size[0] > tile.x,
                self.position[1] < tile.bottom,
                self.position[1] + self.size[1] > tile.y
            ]
        
            if all(conditions):
                collisions.append(tile)
        
        return collisions

    def handle_collisions(self, tiles):
        #collisions - x first, then y
        for i in range(2):
            self.collision[i] = False
            self.position[i] += self.velocity[i]
            
            for collision in self.get_collisions(tiles):
                if self.velocity[i] > 0:
                    self.position[i] = collision[i] - self.size[i]
                else:
                    #0 + 2 = 2 (w), 1 + 2 = 3 (h)
                    #we're finding right / bottom of rect respectively.
                    self.position[i] = collision[i] + collision[i + 2]

                #reset velocity
                self.collision[i] = ((int(self.velocity[i] > 0) * 2) - 1)
                self.velocity[i] = 0

    
    def handle_event(self, event):
        pass
    
    def tick(self, dt):
        #apply gravity
        self.velocity[1] += utils.GRAVITY * dt

        #handle collisions
        self.handle_collisions(self.state.tiles)
        
    def draw(self, surface):
        pass