NEIGHBOR_OFFSETS = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (0, 0), (-1, -1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'} #lookup in set is efficient than looking up a list

from pygame import Rect

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}       # using dictionaries is easier to fill in spaces at random location than filling "air" in between which is a cluster
        self.offgrid_tiles = []
        
        for i in range(10):
            self.tilemap[str(3 +i) + ';10'] = {'type' : 'grass', 'variant' : 0, 'pos' : (3 + i, 10)}
        for i in range(10):
            self.tilemap['10' + ';' + str(5 + i)] = {'type' : 'stone', 'variant' : 0, 'pos' : (10, 5 + i)}
    
    #method looks around the object if it is "near" the tilemap
    #if our object is bigger in size we need to offest it a bit more
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))  #makes a grid on the location instead of pixels
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])  #checking location and converting to str loc to see tilemap later
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
            
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
            
        