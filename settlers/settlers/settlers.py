from game import model, board as gameboard
import random as rnd

from collections import defaultdict
        
class Player(object):
    
    def __init__(self, name, ai_control):
        self.name = name
        self.init_structures()
        self.init_cards()
        self.brain = ai_control
        
    def init_structures(self):
        init_st = lambda x: model.init_structure(self, x)
        self.roads = init_st(model.ROAD)
        self.settlements = init_st(model.SETTLEMENT)
        self.cities = init_st(model.CITY)
        self.struct_map = {model.ROAD: self.roads, model.SETTLEMENT:self.settlements, model.CITY:self.cities}
        
    def init_cards(self):
        self.hand = list()
        self.face_down_development_cards = list()
        self.face_up_development_cards = list()
        
    def add_resources(self, resources):
        self.hand.append(resources)
        
    def remove_resources(self, resources):
        removed_resources = list()
        for res in resources:
            if res in self.hand:
                removed_resources.append(removed_resources)
                self.hand.remove(res)
        return removed_resources
        
    def remove_resource(self, resource_type, max_qty=-1):
        removed_resources = list()
        max_qty = max_qty if max_qty >= 0 else self.hand.count(resource_type)
        for idx in xrange(min(max_qty, self.hand.count(resource_type))):
            removed_resources.append(resource_type)
            self.hand.remove(resource_type)
        return removed_resources
        
    def build_structure(self, structure_type, location):
        available = filter(lambda x: not x.on_board, self.struct_map[structure_type])
        if available:
            using = rnd.choice(available)
            using.add_to_board(location)
            
    def remove_structure(self, structure_type, location=None):
        desired_structure = filter(lambda x: x.on_board and x.location == location if location else True, self.struct_map[structure_type])
        desired_structure.remove_from_board()
        
        
                
    
def roll(num_die=2, num_sides=6):
    return sum([ rnd.randint(1, num_sides) for idx in xrange(num_die) ])
    
class Bank(object):
    
    def __init__(self, initial_size):
        self.bank = reduce(lambda x,y: x+y, [ [res] * initial_size for res in model.RESOURCES ])
        
        
    def trade(self, player, offer, request):
        if self.is_valid_trade(player, offer, request):
            getting = player.remove_resources(offer)
            giving = list()
            for req_item in request:
                if not req_item in self.bank:
                    return False
                else:
                    self.bank.remove(req_item)
                    giving.append(req_item)
            player.add_resources(giving)
            self.bank.extend(getting)
            return True
        else:
            return False
        
    def is_valid_trade(self, player, offer, request):
        return True
        
    def get_resources(self, resource_type, quantity):
        res_del = list()
        for idx in xrange(quantity):
            if resource_type in self.bank:
                res_del.append(resource_type)
                self.bank.remove(resource_type)
            else:
                break
        return res_del
    
    def get_resource(self, resource):
        if resource in self.bank:
            self.bank.remove(resource)
            return resource
        else:
            return None


def find_longest_road(road_segments):
    
    return max([ _find_longest_road(rs, filter(lambda rem_road_seg: rem_road_seg != rs, road_segments)) for rs in road_segments ])
    
def _find_longest_road(current_road, remaining_segments):
    
    vertices = reduce(lambda a,b: a + b, [cr_seg.location for cr_seg in current_road ])
    endpoints = filter(lambda c: vertices.count(c) == 1, vertices)
    
    recursive_results = list()
    for rem_seg in remaining_segments:
        for vertex in rem_seg.location:
            if vertex in endpoints:
                recursive_results.append(current_road + [vertex], filter(lambda rrs: rrs != rem_seg, remaining_segments))
    return max([ len(rec_res) for rec_res in recursive_results ])

class Game(object):
    
    def __init__(self, players, game_board):
        self.players = players
        self.tiles, self.vertices = gameboard.get_tiles_and_vertices(game_board)
        self.game_board = game_board
        self.bank = Bank(model.BANK_SIZE)
        self.victory_points = dict(zip(self.players, [0] * len(self.players)))
        self.longest_road = None
        self.largest_army = None
        self.winner = None
        
        
    def play(self):
        # do initial placement
        self.turn_order = sorted(self.players, key=lambda x: roll())
        
        self.initial_placement()
        #self.play_game()
        
        
    def play_game(self):
        
        active_player_index = 0
        
        while not self.is_game_over():
            active_player = self.turn_order[active_player_index % len(self.players)]
            production_roll = roll()
            self.handle_production(production_roll, active_player)
            
    
        
    def update_victory_points(self):
        victory_points = dict()
        max_road_length = dict()
        for player in self.players:
            total = 0
            for vp_structure in player.settlements + player.cities:
                total += model.VICTORY_POINTS[vp_structure.type]
            
        # determine longest road
        player_roads = sorted(zip(self.players, [ find_longest_road(p.roads) for p in self.players ]), key=lambda x: x[1])
        if filter(lambda pl_rd: pl_rd[1] >= 5, player_roads):
            player_with_longest_road = player_roads[-1][0]
            victory_points[player_with_longest_road] += 2
            
        self.victory_points = victory_points
        
    def is_game_over(self):
        self.update_victory_points()
        threshold = model.VICTORY_POINTS_TO_WIN
        for player, points in self.victory_points.iteritems():
            if points >= threshold:
                self.winner = player
                return True
        return False
        
    def initial_placement(self):
        # determine turn order
        
        placement_order = self.turn_order + [ to for to in reversed(self.turn_order) ]
        
        last_placement_location = dict()
        for placing_player in placement_order:
            # place settlement
            location = placing_player.brain.choose_initial_placement(model.SETTLEMENT, self)
            valid_location = not location.occupied and not reduce(lambda a,b: a or b, [ ln.occupied for ln in location.neighbors)])
            while not valid_location:
                location = placing_player.brain.choose_initial_placement(model.SETTLEMENT, self)
            placing_player.build_structure(model.SETTLEMENT, location)
            # place road
            road_location = placing_player.brain.choose_initial_placement(model.ROAD, self, choice_set=([ (location, ln) for ln in location.neighbors ]))
            placing_player.build_structure(model.ROAD, road_location)
            
            last_placement_location[placing_player] = location
            
        for player, last_location in last_placement_location.iteritems():
            for tile in filter(lambda x: x.type in model.RESOURCES, last_location.tiles):
                player.add_resource(self.bank.get_resource(tile.type))
        
        

    
    
    