from settlers import RESOURCE_DIR as IMG_DIR
from settlers.game import model

import Image, os

tile_images = [ Image.open( os.path.join(IMG_DIR, '%s.png' % tile_type.lower()) ) for tile_type in model.TILE_TYPES ]

tile_img_map = dict(zip(model.TILE_TYPES, tile_images))

def get_map_image(tile_map):
    
    tw, th = tile_images[0].size
    print tile_images[0].size
    
    tile_screen_coords = list()
    
    for x_idx, tile_column in tile_map.iteritems():
        for y_idx, tile in tile_column.iteritems():
            sx = int(tw * x_idx * (0.75))
            sy = int(th * (0.5*x_idx + y_idx))
            tile_screen_coords.append( ((sx, sy), tile_img_map[tile.type]))
            
    x_coords = [ s_coord[0] for s_coord, tile in tile_screen_coords ]
    y_coords = [ s_coord[1] for s_coord, tile in tile_screen_coords ]
    max_x, min_x = max(x_coords), min(x_coords)
    max_y, min_y = max(y_coords), min(y_coords)
    
    print 'x: %d - %d\ny: %d - %d' % (min_x, max_x, min_y, max_y)
    
    map_img_size = (max_x - min_x + tw, max_y - min_y + th)
    
    map_img = Image.new('RGBA', map_img_size)
    for screen_coord, tile_img in tile_screen_coords:
        map_img.paste(tile_img, screen_coord, tile_img)
        
    return map_img