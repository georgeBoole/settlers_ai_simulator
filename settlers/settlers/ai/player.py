import abc
from settlers.game import model

PASS = model.PASS_PRIORITY

class PlayerAI(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def build_settlement(self, open_locations, game_state):
        """Pick a location to build a settlement on"""
        return
        
        
    @abc.abstractmethod
    def build_city(self, existing_settlement_locations, game_state):
        """Select which location to build your city"""
        return
        
    @abc.abstractmethod
    def build_road(self, open_road_locations, game_state):
        """Select which pair of vertices to build your road on"""
        return
        
        
    @abc.abstractmethod
    def discard_half(self, hand, game_state):
        """discard half of your hand to the bank, return a sequence of cards 
        from your hand equal to half your hands size rounded down"""
        return
        
    @abc.abstractmethod
    def choose_initial_placement(self, structure_type, game_state, choice_set=None):
        """Return a location appropriate for the specified structure."""
        return
        
    @abc.abstractmethod
    def use_knight_pre_roll(self, game_state):
        """Return True to play a knight before the production roll"""
        return
        
    @abc.abstractmethod
    def move_robber(self, game_state):
        """Return a Tile that the robber can move to as well as the player you wish to steal from
            Return a sequence of (DestinationTile, PlayerToStealFrom)
        """
        return
        
    @abc.abstractmethod
    def play_development_card(self, development_cards, game_state):
        """Return a development card from your hand or PASS_PRIORITY to do nothing """
        return
        
    @abc.abstractmethod
    def offer_domestic_trade(self, game_state):
        """Return a trade offer or PASS_PRIORITY to do nothing. Trade offer looks like (offer, demand)"""
        return
        
    @abc.abstractmethod
    def consider_domestic_trade(self, offering_player, offer, demand):
        """Return a True to accept the trade and a False to reject it"""
        return
        
    @abc.abstractmethod
    def buy(self, possible_purchases, game_state):
        """Return one of the items in possible purchases or return PASS to do nothing """
        return
        
    @abc.abstractmethod
    def bank_trade(self, game_state):
        """Return a tuple that looks like this (offer, demand)"""
        
        
        