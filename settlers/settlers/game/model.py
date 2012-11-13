from collections import Iterable

RESOURCES = (BRICK, ORE, WOOD, WHEAT, SHEEP) = ('Brick', 'Ore', 'Lumber', 'Grain', 'Wool')
WATER = 'Water'
DESERT = 'Desert'

TILE_TYPES = RESOURCES + (WATER, DESERT)

def _cost(amounts):
    return dict(zip(RESOURCES, amounts))


STRUCTURES = (ROAD, SETTLEMENT, CITY) = ('Road', 'Settlement', 'City')
CARDS = (DEVELOPMENT_CARD, ) = ('Development Card', )
BUYABLE_ITEMS = STRUCTURES + CARDS
BANK_SIZE = 19

COST = {
    ROAD:_cost((1,0,1,0,0)),
    SETTLEMENT:_cost((1,0,1,1,1)),
    CITY:_cost((0,3,0,2,0)),
    DEVELOPMENT_CARD:_cost((0,1,0,1,1))
}

QUANTITY = {
    ROAD:15,
    SETTLEMENT:5,
    CITY:4,
    DEVELOPMENT_CARD:25
}

VICTORY_POINTS_TO_WIN = 10

VICTORY_POINTS = {
    ROAD:0, SETTLEMENT:1, CITY:2, DEVELOPMENT_CARD:0
}

class Structure(object):
    
    def __init__(self, owner, structure_type):
        self.owner = owner
        self.type = structure_type
        self.on_board = False
        self.location = None
        
    def add_to_board(self, location):
        self.location = location
        if not isinstance(self.location, Iterable):
            self.location.occupied = True
        self.on_board = True
        
    def remove_from_board(self):
        self.on_board = False
        if not isinstance(self.location, Iterable):
            self.location.occupied = False
        
def init_structure(owner, structure_type):
    return [Structure(owner, structure_type) for idx in xrange(QUANTITY[structure_type])]
    