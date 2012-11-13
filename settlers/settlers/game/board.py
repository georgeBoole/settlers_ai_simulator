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
    
    vertex_names = ('va', 'vb', 'vc', 'vd', 've', 'vf')
    neighbor_names = ('top', 'top_right', 'bottom_right', 'bottom', 'bottom_left', 'top_left')
    
    def __init__(self, tile_type, production_number):
        self.type = tile_type
        self.production = production_number
        self.neighbors = None
        self.vertices = None
        self.top = None
        self.bottom = None
        self.top_right = None
        self.top_left = None
        self.bottom_left = None
        self.bottom_right = None
        self.va, self.vb, self.vc, self.vd, self.ve, self.vf = [None] * 6
    
    # ASSUMING TOP NEIGHBOR FIRST REST CLOCKWISE    
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.top, self.top_right, self.bottom_right, self.bottom, self.bottom_left, self.top_left = self.neighbors
        
        
    # ASSUMING TOP LEFT VERTEX FIRST REST CLOCKWISE
    def set_vertices(self, vertices):
        self.vertices = vertices
        self.va, self.vb, self.vc, self.vd, self.ve, self.vf = self.vertices
            
    def __str__(self):
        if self.production > 0:
            return '<production: %d, type: %s>' % (self.production, self.type)
        else:
            return '<type: %s>' % self.type


class Vertex(object):
    
    def __init__(self, tiles=None):
        self.occupied = False
        self.occupier = None
        self.neighbors = None
        self.tiles = tiles
        
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        
    def set_tiles(self, tiles):
        self.tiles = tiles
        
    def set_occupier(self, occupier):
        if not self.occupied:
            self.occupied = True
        self.occupier = occupier
        
    def __str__(self):
        return 'Vertex %d, occupied: %s' % (id(self), str(self.occupied))
        
    
neighbor_coords = [
    (0,-1), (1,-1), (1,0), (0,1), (-1,1), (-1,0)
]

vmap = {
    'va':( ('top_left', 'vc'), ('top', 've') ),
    'vb':( ('top', 'vd'), ('top_right', 'vf') ),
    'vc':( ('top_right', 've'), ('bottom_right', 'va') ),
    'vd':( ('bottom_right', 'vf'), ('bottom', 'vb') ),
    've':( ('bottom', 'va'), ('bottom_left', 'vc') ),
    'vf':( ('bottom_left', 'vb'), ('top_left', 'vd') )
}

tmap = {
    'va':('top_left', 'top'),
    'vb':('top', 'top_right'),
    'vc':('top_right','bottom_right'),
    'vd':('bottom_right','bottom'),
    've':('bottom', 'bottom_left'),
    'vf':('bottom_left', 'top_left')
}
    

def _get_neighbor_coords(x,y):
    return [ (x+dx, y+dy) for dx,dy in neighbor_coords ]


def get_tiles_and_vertices(game_board):
    tile_set = reduce(lambda a,b: a + b, [ xvalue.values() for xvalue in game_board.values() ])
    vertex_set = set(reduce(lambda c,d: c + d, [t.vertices for t in tile_set]))
    return tile_set, vertex_set
    
def build_map():
    tile_label_list_list = [ [TT] * TILE_QUANTITY[TT] for TT in TILE_QUANTITY.keys()]
    tile_label_list = [ tile_label for single_type_list in tile_label_list_list for tile_label in single_type_list ]
    rnd.shuffle(tile_label_list)
    
    prod_nums = list(PRODUCTION_NUMBERS)
    rnd.shuffle(prod_nums)
    #vertex_memo = ddict(lambda: ddict(lambda: ddict(lambda: Vertex())))
    
    tile_map = ddict(dict)
    tiles = list()
    for tile_x, tile_y in resource_tile_coords:
        new_tile_type = tile_label_list.pop()
        new_tile_production = prod_nums.pop() if not new_tile_type == DESERT else 0
        new_tile = Tile(new_tile_type, new_tile_production)
        tile_map[tile_x][tile_y] = new_tile
        tiles.append(new_tile)
        
    for tx, ty in resource_tile_coords:
        neighbor_coords = _get_neighbor_coords(tx, ty)
        neighbors = [ tile_map[nx][ny] if (nx,ny) in resource_tile_coords else None for (nx,ny) in neighbor_coords ]
        tile_map[tx][ty].set_neighbors(neighbors)
    
    #vertex_memo = ddict(lambda: ddict(lambda: ddict(lambda: Vertex())))
    
    for tile in tiles:
        
        vertices = list()
        for vertex_name in Tile.vertex_names:
            # check if vertex exists under alias, if not make it
            aliases = vmap[vertex_name]
            found_aliased_vertex = None
            other_tiles = list()
            for neighbor_name, neighbor_vertex_name in aliases:
                neighbor = getattr(tile, neighbor_name)
                if not neighbor:
                    continue
                else:
                    other_tiles.append(neighbor)
                possible_vertex = getattr(neighbor, neighbor_vertex_name)
                if possible_vertex:
                    found_aliased_vertex = possible_vertex
                    break
            if found_aliased_vertex:
                vertices.append(found_aliased_vertex)
            else:
                new_vertex = Vertex(tiles=[ other_tiles[x] if x < len(other_tiles) else None for x in xrange(3)])
                vertices.append(new_vertex)
                
        tile.set_vertices(vertices)
        
    
    
    vert_neigh_map = {
        0: lambda t: [t.vb, t.vf, t.top.vf if t.top else t.top_left.vc if t.top_left else None],
        1: lambda t: [t.va, t.vc, t.top.vc if t.top else t.top_right.va if t.top_right else None],
        2: lambda t: [t.vb, t.vd, t.top_right.vd if t.top_right else t.bottom_right.vb if t.bottom_right else None],
        3: lambda t: [t.ve, t.vc, t.bottom_right.ve if t.bottom_right else t.bottom.vc if t.bottom else None],
        4: lambda t: [t.vf, t.vd, t.bottom_left.vd if t.bottom_left else t.bottom.vf if t.bottom else None],
        5: lambda t: [t.va, t.ve, t.top_left.ve if t.top_left else t.bottom_left.va if t.bottom_left else None]
    }
    vertex_processed = set()
    
    for tile in tiles:
        
        for vidx, vertex in enumerate(tile.vertices):
            if vertex in vertex_processed:
                continue
            elif vertex:
                neighbor_set = vert_neigh_map[vidx](tile)
                vertex.set_neighbors(neighbor_set)
                vertex_processed.add(vertex)
                
            
            
    return tile_map
    
def main():
    #print '\n'.join([ '%d, %d' % nbc for nbc in _get_neighbor_coords(1,0)])
    build_map()
    
if __name__ == '__main__':
    main()