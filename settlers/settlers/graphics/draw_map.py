from settlers import RESOURCE_DIR as IMG_DIR
from settlers.game import model

import Image, os

tile_images = [ Image.open( os.path.join(IMG_DIR, '%s.png' % tile_type.lower()) ) for tile_type in model.TILE_TYPES ]



def get_map_image(tile_map):
    
    tw, th = tile_images[0].size
    
    tile_screen_coords = list()
    
    for x_idx, tile_column in tile_map.iteritems():
        for y_idx, tile in tile_column.iteritems():
            sx = int(tw * x_idx * (0.75))
            sy = int(th * (0.5*x_idx + y_idx))
            tile_screen_coords.append( ((sx, sy), tile))
            
    print tile_screen_coords
    