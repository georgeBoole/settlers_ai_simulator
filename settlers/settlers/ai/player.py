import abc

class PlayerAI(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def choose_initial_placement(self, structure_type, game_state, choice_set=None):
        """Return a location appropriate for the specified structure."""
        return
        