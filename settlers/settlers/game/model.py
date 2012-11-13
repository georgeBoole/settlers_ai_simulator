from collections import Iterable

RESOURCES = (BRICK, ORE, WOOD, WHEAT, SHEEP) = ('Brick', 'Ore', 'Lumber', 'Grain', 'Wool')
WATER = 'Water'
DESERT = 'Desert'

TILE_TYPES = RESOURCES + (WATER, DESERT)

def _cost(amounts):
    return dict(zip(RESOURCES, amounts))


STRUCTURES = (ROAD, SETTLEMENT, CITY) = ('Road', 'Settlement', 'City')
CARDS = (DEVELOPMENT_CARD, ) = ('Development Card', )

DEVELOPMENT_CARDS = (KNIGHT, ROAD_BUILDING, VICTORY_POINT_CARD, YEAR_OF_PLENTY, MONOPOLY) = ('Knight', 'Road Building', 'Victory Point', 'Year of Plenty', 'Monopoly')

DEVELOPMENT_CARD_QUANTITY = {
    KNIGHT:14,
    ROAD_BUILDING:2,
    VICTORY_POINT_CARD:5,
    YEAR_OF_PLENTY:2,
    MONOPOLY:2
}

PASS_PRIORITY = 'PASS'

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

ROBBER_TURN_THRESHOLD = 2
MAX_HAND_SIZE = 7

class Robber(object):
    
    def __init__(self, tile):
        self.home_tile = tile
        self.tile = tile
        self.active = False
        
    def move_to(self, new_tile):
        if not self.active:
            self.active = True
        self.tile = new_tile
        
    def __str__(self):
        return '%sRobber @ %s' % ('Active ' if self.active else 'Inactive ', self.tile)
    
class Structure(object):
    
    def __init__(self, owner, structure_type):
        self.owner = owner
        self.type = structure_type
        self.on_board = False
        self.location = None
        
    def add_to_board(self, location):
        self.location = location
        if self.location and not isinstance(self.location, Iterable):
            self.location.set_occupier(self)
        self.on_board = True
        
    def remove_from_board(self):
        self.on_board = False
        if not isinstance(self.location, Iterable):
            self.location.occupied = False
            self.location.occupier = None
        
def init_structure(owner, structure_type):
    return [Structure(owner, structure_type) for idx in xrange(QUANTITY[structure_type])]


def get_buyable_items(resource_stack):
    buyables = list()
    for item, cost in COST.iteritems():
        can_buy = True
        for res, qty in cost.iteritems():
            if resource_stack.count(res) < qty:
                can_buy = False
                break
        if can_buy:
            buyables.append(item)
    return buyables
        
        
          