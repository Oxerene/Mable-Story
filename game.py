import pygame, sys, random, os
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import load_image, load_images, Animation
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
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background' : load_image('background/bg.png'),
            'clouds' : load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=10),
            'player/run' : Animation(load_images('entities/player/run'), img_dur=8),
            'player/roll' : Animation(load_images('entities/player/roll'), loop=False),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/attack' : Animation(load_images('entities/player/attack'), img_dur= 5),
            'enemy/idle' : Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run' : Animation(load_images('entities/enemy/run'), img_dur=10),
            'enemy/attack' : Animation(load_images('entities/enemy/attack'), img_dur = 7),
            'enemy/death' : load_image('entities/enemy/death/03.png')
        }
            
        self.clouds = Clouds(self.assets['clouds'])
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.level = 0
        self.load_level(self.level)
        
        self.screenshake = 0
        
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        
        self.player = Player(self, (50, 50), (15, 19))
        
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (22, 15)))

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def run(self):
        #game loop
        while True:
            self.display.blit(self.assets['background'], (0, 0))       #refreshes the screen to default display as well as remove trail issue with movement
            
            self.screenshake = max(0, self.screenshake - 1)
            
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 60:
                    self.load_level(self.level)
            
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                    self.dead = 0

            if self.dead <= 60:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = render_scroll)
                if self.player.killed:
                    self.dead += 1
                    self.screenshake = max(16, self.screenshake)

            
            for event in pygame.event.get(): #interact with the windows and get inputs
                #checks to see if we pressed X(cross) on windows
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.attack()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.attack()
                
                #check movement by event listening to Key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump()
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:   
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
            
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2 )
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
            pygame.display.update()         #calling update function to update the screen frequently to avoid black screen
            self.clock.tick(60)             #tries to run the loop at fixed fps

Game().run()