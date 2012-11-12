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
    
    road_problems = list()
    for p in players:
        active_settlements = filter(lambda x: x.on_board, p.settlements)
        #print '%s has %d active settlements' % (p.name, len(active_settlements))
        for r in filter(lambda x: x.location, p.roads):
            start, end = r.location
            if not start in end.neighbors:
                road_problems.append( (p, r) )
                
    return road_problems
            
    
    
def main():
    rp = test_game()
    for p, r in rp:
        print '%s had problem with %s\n\t%s' % (p.name, str(r), 's_tiles: %s\te_tiles: %s' % ([str(st) for st in r.location[0].tiles], [str(et) for et in r.location[1].tiles]))
    #for road_problems in [test_game() for idx in xrange(10)]:
    #    print 'game:\n%s' % '\n'.join( ['%s\t%s' % pr for pr in road_problems ])
    
if __name__ == '__main__':
    main()