import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)     #easier to work with lists than tuple for now
        self.size = size
        self.velocity = [0, 0]   #derivative of pos is velocity ad derrivative of velocity is acceleration
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    #make the entity move by however much we want by taking velocity into account
    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False} #check which direction the collision is happening 
        #taking vel. and movement into account creating a vector to keep track of it
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        #updating object's position with the new vector
        self.pos[0] += frame_movement[0] #x-axis
        #managing 1 axis movement at once 
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                       
        self.pos[1] += frame_movement[1] #y-axis
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1) # increments vel. by 0.5 but stops at 7 which is max vel.

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        