from game import model, board as gameboard
import random as rnd

from collections import defaultdict, Iterable

def report(msg):
    print msg
        
class Player(object):
    
    def __init__(self, name, ai_control):
        report('Creating player object with name %s and ai class %s' % (name, str(ai_control.__class__)))
        self.name = name
        report('Creating structures for player')
        self.init_structures()
        report('Initializing card handling for player')
        self.init_cards()
        report('Setting this players brain to be controlled by AI')
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
        
    def add_development_card(self, devo_card):
        self.face_down_development_cards.append(devo_card)
        
    def add_resources(self, resources):
        self.hand.extend(resources)
        
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
            using = available.pop() if isinstance(available, Iterable) else available
            using.add_to_board(location)
            
    def remove_structure(self, structure_type, location=None):
        desired_structure = rnd.choice(filter(lambda x: x.on_board and x.location == location if location else True, self.struct_map[structure_type]))
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
    return 0
    #vertices = reduce(lambda a,b: a + b, [cr_seg.location for cr_seg in [current_road] ])
    #endpoints = filter(lambda c: vertices.count(c) == 1, vertices)
    #
    #recursive_results = list()
    #for rem_seg in remaining_segments:
    #    for vertex in rem_seg.location:
    #        if vertex in endpoints:
    #            recursive_results.append(current_road + [vertex], filter(lambda rrs: rrs != rem_seg, remaining_segments))
    #return max([ len(rec_res) for rec_res in recursive_results ])

def is_illegal(vertex):
    occupation_status = [ vn.occupied for vn in vertex.neighbors ] + [vertex.occupied]
    any_occupied = reduce(lambda x,y: x or y, occupation_status)
    return any_occupied
    
class Game(object):
    
    def __init__(self, players, game_board):
        report('Creating a Game object')
        self.players = players
        self.tiles, self.vertices = gameboard.get_tiles_and_vertices(game_board)
        self.turns_completed = 0
        self.game_board = game_board
        report('Creating the bank')
        self.bank = Bank(model.BANK_SIZE)
        
        desert_tile = filter(lambda x: x.type == model.DESERT, self.tiles)
        self.robber = model.Robber(desert_tile if desert_tile else rnd.choice(self.tiles))
        report('Initializing bookkeeping variables')
        self.victory_points = dict(zip(self.players, [0] * len(self.players)))
        self.longest_road = None
        self.largest_army = None
        self.winner = None
        
        
    def play(self):
        # do initial placement
        report('Starting game, determining turn order...')
        self.turn_order = sorted(self.players, key=lambda x: roll())
        report('Turn order is %s' % ','.join([p.name for p in self.turn_order]))
        
        report('Beginning initial placement')
        self.initial_placement()
        report('Finished initial placement, beginning game')
        self.play_game()
        
    def steal_resource(self, thief, victim):
        if not victim or len(victim.hand) == 0:
            return
        resource = rnd.choice(victim.hand)
        victim.hand.remove(resource)
        thief.hand.append(resource)
        
    def handle_production(self):
        production_roll = roll()
        if self.turns_completed < model.ROBBER_TURN_THRESHOLD:
            while production_roll == 7:
                production_roll = roll()
        if production_roll == 7:
            for player in self.players:
                if len(player.hand) > model.MAX_HAND_SIZE:
                    discarded_cards = player.brain.discard_half(player.hand, self)
                    for dc in discarded_cards:
                        player.hand.remove(dc)
            (dst, vic) = self.active_player.brain.move_robber(self)
            self.move_robber(dst, vic)
        else:
            for producing_tile in filter(lambda x: x.production == production_roll and self.robber.tile != x, self.tiles):
                resource_produced = producing_tile.type
                for producing_vertex in filter(lambda y: y, producing_tile.vertices):
                    struct = producing_vertex.occupier
                    if struct:
                        qty = 1 if struct.type == model.SETTLEMENT else 2 if struct.type == model.CITY else 0
                        if qty > 0:
                            struct.owner.add_resources([resource_produced] * qty)
                    
    
    def move_robber(self, dst_tile, victim):
        self.robber.move_to(dst_tile)
        if victim:
            self.steal_resource(self.active_player, victim)
            
    def process_trade(self, offering_player, accepting_player, offer, demand):
        for of in offer:
            offering_player.remove(of)
        for de in demand:
            accepting_player.remove(de)
        offering_player.add_resources(demand)
        accepting_player.add_resources(offer)
        
    def legal_settlement_locations(self, player):
        verts = self.vertices
        all_legals = list()
        for vert in verts:
            if not vert.occupied and reduce(lambda a,b: a and b, [ not v.occupied if v else True for v in vert.neighbors]):
                all_legals.append(vert)
        player_roads = filter(lambda v: v.on_board, player.roads)
        free_road_vertices = set(filter(lambda b: b and not b.occupied, reduce(lambda i,j: i+j, [pr.location for pr in player_roads ])))
        all_legal_settlement_vertices = set(all_legals)
        
        return tuple(free_road_vertices.intersection(all_legal_settlement_vertices))
        
    def road_overlap(self, road_locA, road_locB):
        return reduce(lambda x,y: x and y, [ p in road_locB for p in road_locA ])
        
    def road_overlaps(self, test_road, existing_roads):
        return reduce(lambda y,u: y or u, [ self.road_overlap(test_road, er) for er in existing_roads ])
        
    def legal_road_locations(self, player):
        
        all_roads = reduce(lambda a,b: a + b, [p.roads for p in self.players ])
        on_roads = filter(lambda x: x.on_board, all_roads)
        on_road_locations = [ on_r.location for on_r in on_roads ]
        
        road_anchor_points = player.settlements + player.cities
        
        legals = list()
        for vert_struct in road_anchor_points:
            loc = vert_struct.location
            if not loc:
                continue
            if loc.neighbors:
                for ne in loc.neighbors:
                    if not reduce(lambda c,d: c or d, [self.road_overlap((loc, ne), rl) for rl in on_road_locations ]):
                        legals.append((loc, ne))
        for player_road in filter(lambda z: z.on_board, player.roads):
            for endpoint in filter(lambda u: u, player_road.location):
                neighbors = endpoint.neighbors
                locs = filter(lambda r: not self.road_overlaps(r, on_road_locations), [ (endpoint, n) for n in neighbors ])
                
                if locs:
                    legals.extend(locs) if isinstance(locs, Iterable) else legals.append(locs)
                
        return filter(lambda loc: len(loc) == 2 and loc[0] and loc[1] and loc[0] in loc[1].neighbors , legals)
        
    def buy_item(self, player, item):
        if item == model.SETTLEMENT:
            location = player.brain.build_settlement(self.legal_settlement_locations(player), self)
            player.build_structure(model.SETTLEMENT, location)
        elif item == model.CITY:
            settlement_locations = [ s.location for s in filter(lambda x: x.on_board, player.settlements) ]
            location = player.brain.build_city(settlement_locations, self)
            if not location:
                city_cost = ([model.ORE] * 3) + ([model.WHEAT] * 2)
                player.add_resources(city_cost)
                return
            settlement = location.occupier
            player.remove_structure(model.SETTLEMENT, location)
            player.build_structure(model.CITY, location)
        elif item == model.ROAD:
            road_locations = self.legal_road_locations(player)
            selected_location = player.brain.build_road(road_locations, self)
            player.build_structure(model.ROAD, selected_location)
            
            
        
    def play_game(self):
        active_player_index = 0
                    
        while not self.is_game_over():
            devo_played = False
            self.active_player = self.turn_order[self.turns_completed % len(self.players)]
            active_p = self.active_player
            brain = active_p.brain
            def try_devo_play():
                if not active_p.face_down_development_cards or len(active_p.face_down_development_cards) < 1:
                    return
                devo_play = brain.play_development_card(active_p.face_down_development_cards, self)
                if devo_play != model.PASS_PRIORITY:
                    devo_played = True
                    self.play_development_card(devo_play)
            
            if model.KNIGHT in active_p.face_up_development_cards:
                devo_played = brain.use_knight_pre_roll(self)
                if devo_played:
                    self.play_knight(active_p)
            self.handle_production()
            # now player can play devo, or trade
            
            
            # TRADE PHASE
            domestic_open = True
            bank_open = True
            while domestic_open or bank_open:
                if not devo_played:
                    try_devo_play()
                domestic_open = True
                bank_open = True
                domestic_trade = brain.offer_domestic_trade(self)
                if domestic_trade != model.PASS_PRIORITY:
                    offer, demand = domestic_trade
                    for non_active_player in filter(lambda x: x != active_p, self.players):
                        accepted = non_active_player.brain.consider_domestic_trade(active_p, offer, demand)
                        if accepted:
                            self.process_trade(active_p, non_active_player, offer, demand)
                            break
                else:
                    domestic_open = False
                
                if not devo_played:
                    try_devo_play()
                bank_trade = brain.bank_trade(self)
                if bank_trade != model.PASS_PRIORITY:
                    offer, demand = bank_trade
                    self.bank.trade(active_p, offer, demand)
                else:
                    bank_open = False
                
            
            # BUY PHASE
            
            done_buying = False
            while not done_buying:
                if not devo_played:
                    try_devo_play()
                
                buyable_items = filter(lambda x: x != model.CITY if len(filter(lambda y: y.on_board, active_p.settlements)) < 1 else True, model.get_buyable_items(active_p.hand) )
                if not buyable_items or len(buyable_items) == 0:
                    done_buying = True
                    continue
                purchase = brain.buy(buyable_items, self)
                if purchase != model.PASS_PRIORITY:
                    cost = model.COST[purchase]
                    for resource, qty in cost.iteritems():
                        active_p.remove_resource(resource, max_qty=qty)
                    self.buy_item(active_p, purchase)
                else:
                    if not devo_played:
                        try_devo_play()
                    done_buying = True
            
            self.turns_completed += 1
            #print 'finished with turn %d' % self.turns_completed
        #print 'done with the game, %s won' % self.winner.name
            
            
    def play_knight(self):
        self.active_player.face_down_development_cards.remove(model.KNIGHT)
        self.active_player.face_up_development_cards.append(model.KNIGHT)
        (new_tile, player_to_steal_from) = active_player.brain.move_robber(self)
        self.move_robber(new_tile, player_to_steal_from)
        
    def play_development_card(self, development_card):
        if development_card == model.KNIGHT:
            self.play_knight()
        else:
            self.active_player.face_down_development_cards.remove(development_card)
            self.active_player.face_up_development_cards.append(development_card)
            
        
    def update_victory_points(self):
        victory_points = dict()
        max_road_length = dict()
        for player in self.players:
            total = 0
            for vp_structure in player.settlements + player.cities:
                if vp_structure.on_board:
                    total += model.VICTORY_POINTS[vp_structure.type]
            total += player.face_up_development_cards.count(model.VICTORY_POINT_CARD)
            victory_points[player] = total
        # determine longest road
        player_roads = sorted(zip(self.players, [ find_longest_road(p.roads) for p in self.players ]), key=lambda x: x[1])
        if filter(lambda pl_rd: pl_rd[1] >= 5, player_roads):
            player_with_longest_road = player_roads[-1][0]
            victory_points[player_with_longest_road] += 2
            
        # determine largest army
        max_army = -1
        max_army_player = None
        for player in self.players:
            army = len(filter(lambda x: x == model.KNIGHT, player.face_up_development_cards))
            if army > max_army:
                max_army = army
                max_army_player = player
        if max_army >= 3:
            victory_points[max_army_player] += 2
            
        change_detected = False    
        for p in self.players:
            if self.victory_points[p] != victory_points[p]:
                change_detected=True
        if change_detected:
            print 'Current Standings:\n\t%s' % '\n\t'.join([ '%s %d' % (p.name, vp) for p, vp in victory_points.iteritems() ])
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
        legal_spots = list(self.vertices)
        for placing_player in placement_order:
                
            location = placing_player.brain.choose_initial_placement(model.SETTLEMENT, self, choice_set=legal_spots)
            
            legal_spots.remove(location)
            for n in location.neighbors:
                if n in legal_spots:
                    legal_spots.remove(n)
                    
            placing_player.build_structure(model.SETTLEMENT, location)

            road_location = placing_player.brain.choose_initial_placement(model.ROAD, self, choice_set=([ (location, ln) for ln in filter(lambda x: x, location.neighbors) ]))
            placing_player.build_structure(model.ROAD, road_location)
            
            last_placement_location[placing_player] = location
            
            
        for player, last_location in last_placement_location.iteritems():
            for tile in filter(lambda x: x and x.type in model.RESOURCES, last_location.tiles):
                player.add_resources([self.bank.get_resource(tile.type)])
        
        

    
    
    