#!/usr/bin/env python


class State(object):
    """Represents the state of the game.

    Attributes:
        cells_cnt (int): Amount of cells in the game.
        species_cnt (int): Amount of species in the game.
        iterations_cnt (int): Value of current iteration in the game.
        organism_l (list): Organisms which are currently present in the game.
    """
    def __init__(self, cells_cnt, species_cnt, iterations_cnt, organism_l):
        self.cells_cnt = cells_cnt
        self.species_cnt = species_cnt
        self.iterations_cnt = iterations_cnt
        self.organism_l = organism_l

    def __str__(self):
        return '%(cells)s-%(species)s-%(iterations)s' % {'cells': self.cells_cnt,
                                                         'species' : self.species_cnt,
                                                         'iterations' : self.iterations_cnt}

    def is_valid(self):
        """Validates if state's attributes are valid.

        Mainly checks if the cells, species and iterations are ints and higher or equal to 0.
        Also checks if the organisms are specified.

        Returns:
            bool: True if attributes are valid, False otherwise.
        """
        if not (self.cells_cnt is not None and self.cells_cnt > 0):
            return False

        if not (self.species_cnt is not None and self.species_cnt > 0):
            return False

        if not (self.iterations_cnt is not None and self.iterations_cnt >= 0):
            return False

        if not self.organism_l:
            return False

        return True
