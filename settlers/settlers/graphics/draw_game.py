from settlers import RESOURCE_DIR as IMG_DIR
from settlers.game import model

import Image, ImageFont, ImageDraw, os, colorsys

tile_images = [ Image.open( os.path.join(IMG_DIR, '%s.png' % tile_type.lower()) ) for tile_type in model.TILE_TYPES ]
settlement_mask, city_mask = [ Image.open(os.path.join(IMG_DIR, '%s_mask.png' % structure)) for structure in [model.SETTLEMENT.lower(), model.CITY.lower()]]
tile_img_map = dict(zip(model.TILE_TYPES, tile_images))


board_font = ImageFont.truetype(os.path.join(IMG_DIR, 'roboto', 'Roboto-Black.ttf'), 60)

def vertex_locations(tile_width, tile_height):
    return [
        (tile_width / 4, 0),
        (tile_width * (3.0/4.0), 0),
        (tile_width, tile_height / 2),
        (tile_width * (3.0/4.0), tile_height),
        (tile_width / 4, tile_height),
        (0, tile_height / 2)
    ]

def draw_production(tile_image, production_number):
    if production_number <= 0:
        return tile_image
    tw, th = board_font.getsize(str(production_number))
    iw, ih = tile_image.size
    text_pos = (iw - tw) / 2, (ih - th) / 2
    new_image = Image.new('RGBA', (iw, ih))
    new_image.paste(tile_image, (0,0), tile_image)
    draw = ImageDraw.Draw(new_image)
    draw.rectangle([text_pos, (text_pos[0] + tw, text_pos[1] + th)], fill=(255,255,207))
    text_color = (255,0,0) if production_number == 6 or production_number == 8 else (0,0,0)
    draw.text(text_pos, str(production_number), font=board_font, fill=text_color)
    del draw
    return new_image

def get_map_image(tile_map, sprite_structures=None):
    
    tw, th = tile_images[0].size
    #print tile_images[0].size
    
    vertex_sprite_map = dict([ (structure.location, sprite) for sprite, structure in sprite_structures ])
    
    vert_sprite_draws = list()
    
    tile_screen_coords = list()
    
    vertex_locs = vertex_locations(tw, th)
    
    for x_idx, tile_column in tile_map.iteritems():
        for y_idx, tile in tile_column.iteritems():
            sx = int(tw * x_idx * (0.75))
            sy = int(th * (0.5*x_idx + y_idx))
            tile_image = draw_production(tile_img_map[tile.type], tile.production)
            tile_screen_coords.append( ((sx, sy), tile_image))
            if sprite_structures:
                for vidx, v in enumerate(tile.vertices):
                    if v in vertex_sprite_map:
                        vdx, vdy = vertex_locs[vidx]
                        vert_sprite_draws.append(vertex_sprite_map[v], (sx + vdx, sy + vdy))
            
    x_coords = [ s_coord[0] for s_coord, tile in tile_screen_coords ]
    y_coords = [ s_coord[1] for s_coord, tile in tile_screen_coords ]
    max_x, min_x = max(x_coords), min(x_coords)
    max_y, min_y = max(y_coords), min(y_coords)
    
    #print 'x: %d - %d\ny: %d - %d' % (min_x, max_x, min_y, max_y)
    
    map_img_size = (max_x - min_x + tw, max_y - min_y + th)
    
    map_img = Image.new('RGBA', map_img_size)
    background_image = Image.open(os.path.join(IMG_DIR, 'background.png')).resize(map_img_size)
    map_img.paste(background_image, (0,0))
    for screen_coord, tile_img in tile_screen_coords:
        map_img.paste(tile_img, screen_coord, tile_img)
        
    for sprite_img, screen_loc in vert_sprite_draws:
        map_img.paste(sprite_img, screen_loc, sprite_img)
        
    return map_img

def build_sprite(size, mask, color):
    if mask.size != size:
        mask = mask.resize(size)
        
    color_img = Image.new('RGBA', size, color)
    dst_img = Image.new('RGBA', size)
    dst_img.paste(color_img, (0,0), mask)
    return dst_img


BASE_STRUCTURE_SIZE = 50
SCALE_FACTORS = {model.SETTLEMENT:1.0, model.CITY:1.3}

def render_game(game_state):
    board = game_state.game_board
    colors = [ colorsys.hsv_to_rgb(float(idx)/len(game_state.players)) for idx in xrange(len(players)) ]
    
    
    settlement_size, city_size = [ tuple([SCALE_FACTORS[stype] * BASE_STRUCTURE_SIZE] * 2) for stype in [model.SETTLEMENT, model.CITY] ]
    
    sprite_structure_pairs = list()
    for player, color in zip(game_state.players, colors):
        set_sprite, city_sprite = build_sprite(settlement_size, settlement_mask, color), build_sprite(city_size, city_mask, color)
        on_board_structures = filter(lambda struct: struct.on_board, player.cities + player.settlements)
        for obs in on_board_structures:
            sprite_structure_pairs.append( set_sprite if obs.type == model.SETTLEMENT else city_sprite, obs)
    
    
    board_image = get_map_image(board, sprite_structure_pairs)
    
    return board_image
        