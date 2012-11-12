from settlers import settlers as sim
from settlers.ai import player
from settlers.game import board
from settlers.graphics import draw_game
import random as rnd


class BasicAI(object):
    
    def choose_initial_placement(self, structure_type, game_state, choice_set=None):
        if choice_set:
            return rnd.choice(choice_set)
        else:
            return rnd.choice(list(game_state.vertices))
            
            
player.PlayerAI.register(BasicAI)


def test_game():
    players = [ sim.Player(name, BasicAI()) for name in ('Mike', 'Tits', 'Bitch') ]
    game_map = board.build_map()
    game = sim.Game(players, game_map)
    
    game.play()
    
    game_screenshot = draw_game.render_game(game)
    game_screenshot.show()
    
    for p in players:
        active_settlements = filter(lambda x: x.on_board, p.settlements)
        print '%s has %d active settlements' % (p.name, len(active_settlements))
    
def main():
    test_game()
    
if __name__ == '__main__':
    main()