import pygame, sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init() # initialising pygame

        pygame.display.set_caption("Mable Story")
        self.screen = pygame.display.set_mode((1280, 720)) # resolution of the game
        self.display = pygame.Surface((640, 360))
        self.clock = pygame.time.Clock() # creates an object of clock to maintain fps and time delay required to update display accordingly
        
        # initialising default position for the image (easy to change later with movement)
        self.img_pos = [160, 260]
        self.movement = [False, False] #by default its idle, no movement on x-axis and y-axis
        
        self.assets = {
            'grass' : load_images('platform/grass'),
            'stone' : load_images('platform/stone'),
            'player' : load_image('entities/player/knight.png')
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (13, 19))
        
        self.tilemap = Tilemap(self, tile_size=16)


    def run(self):
        #game loop
        while True:
            self.display.fill((29, 151, 245)) #refreshes the screen as well to remove trail issue with movement
            
            self.tilemap.render(self.display)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)
            
            print(self.tilemap.physics_rects_around(self.player.pos))
            
            for event in pygame.event.get(): #interact with the windows and get inputs
                #checks to see if we pressed X(cross) on windows
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                
                #check movement by event listening to Key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:   
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()         #calling update function to update the screen frequently to avoid black screen
            self.clock.tick(60)                  #tries to run the loop at fixed fps

Game().run()