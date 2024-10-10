import pygame, sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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
            'player' : load_image('entities/player/knight.png'),
            'background' : load_image('background/bg.png'),
            'clouds' : load_images('clouds')
        }
        
        self.clouds = Clouds(self.assets['clouds'])
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (13, 19))
        
        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    def run(self):
        #game loop
        while True:
            self.display.blit(self.assets['background'], (0, 0))                   #refreshes the screen to default display as well as remove trail issue with movement
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset = render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = render_scroll)
            
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
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:   
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()         #calling update function to update the screen frequently to avoid black screen
            self.clock.tick(90)             #tries to run the loop at fixed fps

Game().run()