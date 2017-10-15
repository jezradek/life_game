#!/usr/bin/env python


class Organism(object):
    """Represents organism in the game.

    Attributes:
        x (int): Coordinate at x axes.
        y (int): Coordinate at y axes.
        species (int): Species identifier.
    """
    def __init__(self, x, y, species):
        self.x = x
        self.y = y
        self.species = species

    def __str__(self):
        return '%(x)s-%(y)s-%(species)s' % {'x': self.x,
                                            'y' : self.y,
                                            'species' : self.species}
