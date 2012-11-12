import settlers

from settlers.game import board
from settlers.graphics import draw_game as draw_map
from settlers import settlers as simulator


def test_map():
    my_map = board.build_map()
    
    #print my_map
    
    my_map_img = draw_map.get_map_image(my_map)
    
    my_map_img.show()
    
def test_game():
    pass
    
    
def main():
    test_map()
    #sprite = generate_settlement_sprite(200, 200, (125, 40, 208))
    #sprite.show()
    
if __name__ == '__main__':
    main()