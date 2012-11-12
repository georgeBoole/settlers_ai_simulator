from collections import defaultdict as ddict
import random as rnd

from model import BRICK, ORE, WOOD, WHEAT, SHEEP, WATER, DESERT

resource_tile_coords = [
    (0,1), (0,2), (0,3),
    (1,0), (1,1), (1,2), (1,3),
    (2,-1), (2,0), (2,1), (2,2), (2,3),
    (3,-1), (3,0), (3,1), (3,2),
    (4,-1), (4,0), (4,1)
]

PRODUCTION_NUMBERS = (2, 12) + reduce(lambda a,b: a + b, [ tuple([x] * 2) for x in [3,4,5,6,8,9,10,11] ])

TILE_QUANTITY = {
    BRICK:3,
    ORE:3,
    WOOD:4,
    WHEAT:4,
    SHEEP:4,
    DESERT:1
}


class Tile(object):
    NEIGHBOR_DIRECTIONS = ('up', 'up_right', 'down_right', 'down', 'down_left', 'up_left')
    VERTICES = ('a', 'b', 'c', 'd', 'e', 'f')
    
    def __init__(self, tile_type, production_number):
        self.type = tile_type
        self.production = production_number
        for nd in Tile.NEIGHBOR_DIRECTIONS:
            setattr(self, nd, None)
            
        for vur_tiss_cee in Tile.VERTICES:
            setattr(self, vur_tiss_cee, None)
            
    def __str__(self):
        if self.production > 0:
            return '<production: %d, type: %s>' % (self.production, self.type)
        else:
            return '<type: %s>' % self.type
            
class Vertex(object):
    
    
    def __init__(self):
        self.occupant = None
    
neighbor_coords = [
    (0,-1), (1,-1), (1,0), (0,1), (-1,1), (-1,0)
]

#NEIGHBOR_TO_COORDS = dict(zip(Tile.NEIGHBOR_DIRECTIONS, neighbor_coords))
    

def _get_neighbor_coords(x,y):
    return filter(lambda neighbor_tile: neighbor_tile in resource_tile_coords, [ (x+dx, y+dy) for dx,dy in neighbor_coords ])

def build_map():
    tile_label_list_list = [ [TT] * TILE_QUANTITY[TT] for TT in TILE_QUANTITY.keys()]
    tile_label_list = [ tile_label for single_type_list in tile_label_list_list for tile_label in single_type_list ]
    rnd.shuffle(tile_label_list)
    
    prod_nums = list(PRODUCTION_NUMBERS)
    rnd.shuffle(prod_nums)
    #vertex_memo = ddict(lambda: ddict(lambda: ddict(lambda: Vertex())))
    
    tile_map = ddict(dict)
    for tile_x, tile_y in resource_tile_coords:
        new_tile_type = tile_label_list.pop()
        new_tile_production = prod_nums.pop() if not new_tile_type == DESERT else 0
        tile_map[tile_x][tile_y] = Tile(new_tile_type, new_tile_production)
        
        
    return tile_map
    
def main():
    #print '\n'.join([ '%d, %d' % nbc for nbc in _get_neighbor_coords(1,0)])
    build_map()
    
if __name__ == '__main__':
    main()