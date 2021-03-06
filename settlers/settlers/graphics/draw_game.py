from settlers import RESOURCE_DIR as IMG_DIR
from settlers.game import model

import Image, ImageFont, ImageDraw, os, colorsys

tile_images = [ Image.open( os.path.join(IMG_DIR, '%s.png' % tile_type.lower()) ) for tile_type in model.TILE_TYPES ]
settlement_mask, city_mask = [ Image.open(os.path.join(IMG_DIR, '%s_mask.png' % structure)) for structure in [model.SETTLEMENT.lower(), model.CITY.lower()]]
tile_img_map = dict(zip(model.TILE_TYPES, tile_images))


board_font = ImageFont.truetype(os.path.join(IMG_DIR, 'roboto', 'Roboto-Black.ttf'), 60)

def pil_color(color):
    return tuple([ int(c * 255.0) for c in color ])

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

def get_map_image(tile_map, sprite_structures=None, roads=None):
    
    tw, th = tile_images[0].size
    #print tile_images[0].size
    
    vertex_sprite_map = dict([ (structure.location, sprite) for sprite, structure in sprite_structures ])
    
    vert_sprite_draws = list()
    
    all_road_vertices = list(set(reduce(lambda a,b: a + b, [ location for location, color in roads ])))
    COORD_UNKNOWN = (-1, -1)
    road_vertex_coords = dict(zip(all_road_vertices, [COORD_UNKNOWN] * len(all_road_vertices)))
    
    tile_screen_coords = list()
    
    vertex_locs = vertex_locations(tw, th)
    
    x_offset, y_offset = 80, 80
    for x_idx, tile_column in tile_map.iteritems():
        for y_idx, tile in tile_column.iteritems():
            sx = int(tw * x_idx * (0.75)) + x_offset/2
            sy = int(th * (0.5*x_idx + y_idx)) + y_offset/2
            tile_image = draw_production(tile_img_map[tile.type], tile.production)
            tile_screen_coords.append( ((sx, sy), tile_image))
            if sprite_structures:
                for vidx, v in enumerate(tile.vertices):
                    if v in vertex_sprite_map:
                        vdx, vdy = vertex_locs[vidx]
                        sprite = vertex_sprite_map[v]
                        vert_sprite_draws.append((sprite, (int(sx + vdx - (sprite.size[0]/2)), int(sy + vdy - (sprite.size[1]/2)))))
            if roads:
                for vidx, v in enumerate(tile.vertices):
                    if v in road_vertex_coords:
                        vdx, vdy = vertex_locs[vidx]
                        vloc = int(sx+vdx), int(sy+vdy)
                        road_vertex_coords[v] = vloc
                    
            
            
    x_coords = [ s_coord[0] for s_coord, tile in tile_screen_coords ]
    y_coords = [ s_coord[1] for s_coord, tile in tile_screen_coords ]
    max_x, min_x = max(x_coords), min(x_coords)
    max_y, min_y = max(y_coords), min(y_coords)
    
    #print 'x: %d - %d\ny: %d - %d' % (min_x, max_x, min_y, max_y)
    
    map_img_size = (max_x - min_x + tw + x_offset, max_y - min_y + th + y_offset)
    
    map_img = Image.new('RGBA', map_img_size)
    
    for screen_coord, tile_img in tile_screen_coords:
        map_img.paste(tile_img, screen_coord, tile_img)
        
    draw = ImageDraw.Draw(map_img)
    
    for rd in roads:
        line_points = [ tuple([int(rvc) for rvc in road_vertex_coords[loc]]) for loc in rd[0] ]
        #print line_points
        draw.line(line_points, fill=pil_color(rd[1]), width=8)
    
    del draw
    
    for sprite_img, screen_loc in vert_sprite_draws:
        map_img.paste(sprite_img, screen_loc, sprite_img)
    
    screenshot = Image.new('RGBA', (int(map_img_size[0] * 1.3), int(map_img_size[1] * 1.3)))
    background_image = Image.open(os.path.join(IMG_DIR, 'background.png')).resize(screenshot.size)
    screenshot.paste(background_image, (0,0))
    miw, mih = map_img_size
    ssw, ssh = screenshot.size
    
    screenshot.paste(map_img, ((ssw-miw)/2, (ssh-mih)/2), map_img)
    return screenshot

def build_sprite(size, mask, color):
    isize = [ int(size_el) for size_el in size ]
    
    if mask.size != isize:
        mask = mask.resize(isize)
    color_img = Image.new('RGBA', isize, pil_color(color))
    dst_img = Image.new('RGBA', isize)
    dst_img.paste(color_img, (0,0), mask)
    return dst_img


BASE_STRUCTURE_SIZE = 50
SCALE_FACTORS = {model.SETTLEMENT:1.0, model.CITY:1.3}

def render_game(game_state):
    board = game_state.game_board
    colors = [ colorsys.hsv_to_rgb(float(idx)/len(game_state.players), 1.0, 1.0) for idx in xrange(len(game_state.players)) ]
    
    
    settlement_size, city_size = [ tuple([SCALE_FACTORS[stype] * BASE_STRUCTURE_SIZE] * 2) for stype in [model.SETTLEMENT, model.CITY] ]
    
    sprite_structure_pairs = list()
    roads = list()
    for player, color in zip(game_state.players, colors):
        #print '%s is going to be the color %s this game' % (player.name, str(color))
        set_sprite, city_sprite = build_sprite(settlement_size, settlement_mask, color), build_sprite(city_size, city_mask, color)
        on_board_structures = filter(lambda struct: struct.on_board, player.cities + player.settlements)
        on_board_roads = filter(lambda road: road.on_board, player.roads)
        #print '%s has %d structures and %d roads' % (player.name, len(on_board_structures), len(on_board_roads))
        for obs in on_board_structures:
            sprite_structure_pairs.append( (set_sprite if obs.type == model.SETTLEMENT else city_sprite, obs))
        for obr in on_board_roads:
            roads.append((obr.location, color))
    
    
    board_image = get_map_image(board, sprite_structure_pairs, roads)
    
    return board_image
        