RESOURCES = (BRICK, ORE, WOOD, WHEAT, SHEEP) = ('Brick', 'Ore', 'Lumber', 'Grain', 'Wool')
WATER = 'Water'
DESERT = 'Desert'

TILE_TYPES = RESOURCES + (WATER, DESERT)

def _cost(amounts):
    return dict(zip(RESOURCES, amounts))


BUYABLE_ITEMS = (ROAD, SETTLEMENT, CITY, DEVELOPMENT_CARD) = ('Road', 'Settlement', 'City', 'Development Card')

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

