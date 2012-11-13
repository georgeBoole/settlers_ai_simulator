from settlers import settlers as sim
from settlers.ai import player
from settlers.game import board
from settlers.graphics import draw_game
import random as rnd

PASS = player.PASS

class BasicAI(object):
    
    def choose_initial_placement(self, structure_type, game_state, choice_set=None):
        if choice_set:
            return rnd.choice(choice_set)
        else:
            return rnd.choice(list(game_state.vertices))
            
    def build_settlement(self, open_locations, game_state):
        if open_locations:
            return rnd.choice(open_locations)
        
    def build_city(self, existing_settlement_locations, game_state):
        if existing_settlement_locations:
            return rnd.choice(existing_settlement_locations)
        
    def build_road(self, open_road_locations, game_state):
        return rnd.choice(open_road_locations)
        
    def discard_half(self, hand, game_state):
        return rnd.sample(hand, len(hand) / 2)
        
    def use_knight_pre_roll(self, game_state):
        return rnd.choice([True, False])
        
    def move_robber(self, game_state):
        open_tiles = filter(lambda x: x != game_state.robber.tile, game_state.tiles)
        dst = rnd.choice(open_tiles)
        for v in dst.vertices:
            if v.occupier:
                return (dst, v.occupier.owner)
        return (dst, None)
        
    def play_development_card(self, development_cards, game_state):
        return rnd.choice(development_cards)
        
    def offer_domestic_trade(self, game_state):
        return PASS
        
    def consider_domestic_trade(self, offering_player, offer, demand):
        return False
        
    def buy(self, possible_purchases, game_state):
        return rnd.choice(possible_purchases)
        
    def bank_trade(self, game_state):
        return PASS
        

player.PlayerAI.register(BasicAI)


def test_game():
    players = [ sim.Player(name, BasicAI()) for name in ('Jace', 'Chandra', 'Nicol') ]
    game_map = board.build_map()
    game = sim.Game(players, game_map)
    
    game.play()
    
    print 'game over, winner was %s' % game.winner.name
    print 'Points breakdown:'
    for player, victory_points in game.victory_points.iteritems():
        print '%s %d' % (player.name, victory_points)
        
    game_screenshot = draw_game.render_game(game)
    game_screenshot.show()
    
    
def main():
    test_game()
    
if __name__ == '__main__':
    main()