#!/usr/bin/env python


class WorldGrid(object):
    """Encapsulates the living space (grid) for organisms in the game.

    Attributes:
        width (int): Width of x axes.
        height (int): Height of y axes.
    """
    def __init__(self, width, height):
        self.width = width
        self.height= height

        self.grid = self.build() 

    def build(self):
        """Builds the world grid (2d list).

        Returns:
            grid (list): 2 dimensional list.
        """
        return [[None]*self.width for _ in xrange(self.width)]

    def rebuild(self):
        """Rebuilds the world grid (2d list).

        Returns:
            grid (list): 2 dimensional list.
        """
        self.grid = self.build()

    def set_organisms(self, organism_l):
        """Set organisms to the grid.

        Attributes:
            organism_l (list): Organisms which are to be set to the grid.

        Raises:
            WorldGridCoordinatesError: If organisms coordinates (x|y) are not valid.
        """
        for organism in organism_l:
            self.set_organism(organism)

    def set_organism(self, organism):
        """Set organism to the grid.

        Attributes:
            organism (Organism): Organism which is to be set to the grid.

        Raises:
            WorldGridCoordinatesError: If organism coordinates (x|y) are not valid.
        """
        if not self._are_coordinates_valid(organism.x, organism.y):
            raise WorldGridCoordinatesError('Wrong coordinates (x|y) for setting the organism.')

        self.grid[organism.x][organism.y] = organism

    def get_organism_at(self, x, y):
        """Retrieves organism at coordinates x|y.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            organism (Organism): Organism if exist, else None.

        Raises:
            WorldGridCoordinatesError: If coordinates (x|y) are not valid.
        """
        if not self._are_coordinates_valid(x, y):
            raise WorldGridCoordinatesError('Wrong coordinates (x|y) for getting the organism.')

        return self.grid[x][y]

    def get_neighboring_cells_at(self, x, y):
        """Retrieves neighbouring cells for cell at coordinates x|y.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            neighboring_cell_l (list): Neighbouring cells if exist, else empy list.

        Raises:
            WorldGridCoordinatesError: If coordinates (x|y) are not valid.
        """
        if not self._are_coordinates_valid(x, y):
            raise WorldGridCoordinatesError('Wrong coordinates (x|y) for neighboring cells.')

        neighboring_cell_l = []

        if x > 0: 
            neighboring_cell_l.append((x - 1, y))

        if x < self.width - 1:
            neighboring_cell_l.append((x + 1, y))

        if y > 0:
            neighboring_cell_l.append((x, y - 1))

        if y < self.height - 1:
            neighboring_cell_l.append((x, y + 1))

        if x > 0 and y > 0:
            neighboring_cell_l.append((x - 1, y - 1))

        if x < self.width - 1 and y > 0:
            neighboring_cell_l.append((x + 1, y - 1))

        if x > 0 and y < self.height - 1:
            neighboring_cell_l.append((x - 1, y + 1))

        if x < self.width - 1 and y < self.height - 1:
            neighboring_cell_l.append((x + 1, y + 1))

        return neighboring_cell_l

    def _are_coordinates_valid(self, x, y):
        """Validates coordinates at x|y axes.

        Mainly checks if they have positive calue and are inside the predefined grid.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            valid (bool): True if coordinates (x|y) are valid, False otherwise.
        """
        valid = True

        if x < 0 or x >= self.width:
            valid = False
        elif y < 0 or y >= self.height:
            valid = False

        return valid


class WorldGridCoordinatesError(Exception):
    pass
