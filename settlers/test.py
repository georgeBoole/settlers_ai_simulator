import settlers

from settlers.game import board
from settlers.graphics import draw_map

my_map = board.build_map()

#print my_map

my_map_img = draw_map.get_map_image(my_map)

my_map_img.show()