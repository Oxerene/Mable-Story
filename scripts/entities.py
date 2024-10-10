import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)     #easier to work with lists than tuple for now
        self.size = size
        self.velocity = [0, 0]   #derivative of pos is velocity ad derrivative of velocity is acceleration
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}

        self.action = ''
        self.anim_offset = (0, 0)    #used to make offset around image to make up with varying size of images animation
        self.flip = False
        self.set_action('idle')
        
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    # check if the animation has changed 
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
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
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1) # increments vel. by 0.5 but stops at 7 which is max vel.

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.animation.update()
        
    def render(self, surf, offset = (0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
    
    def update(self, tilemap, movement):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        