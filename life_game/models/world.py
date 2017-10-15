#!/usr/bin/env python
from life_game.models.world_grid import WorldGrid, WorldGridCoordinatesError
from life_game.rules.evolution_rules_engine import EngineCanNotEvolveOrganismError


class World(object):
    """Encapsulates organisms and living space in the game.

    Also provides possibility to evolve organisms between iterations.
    Organisms are evolved according to the evolution rules handled by rules engine.

    Attributes:
        world_grid (WorldGrid): Living space for organisms (world grid).
        organism_l (int): Organisms which are currently present in the game.
        rules_engine (EvolutionRulesEngine): Applies evolution rules on organisms.
    """
    def __init__(self, world_grid, organism_l, rules_engine):
        self.world_grid = world_grid
        self.organism_l = organism_l
        self.rules_engine = rules_engine

    @property
    def width(self):
        """int: Width of the world grid."""
        return self.world_grid.width

    @property
    def height(self):
        """int: Height of the world grid."""
        return self.world_grid.height

    def populate_initial_organisms(self):
        """Populates world with initial organisms.

        Public method which have to be called after the world is constructed.

        Resolves initial conflicts, by definition:
        `If two organisms occupy one element, one of them must
        die (chosen randomly) (only to resolve initial conflicts).`

        Attributes:
            organism (Organism): Organism on which the rules will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments are not used for this rule.

        Returns:
            initial_conflict (bool): True if initial conflict occurred, False otherwise.

        Raises:
            WorldInternalError: If organisms provided to the game are not valid.
        """
        initial_conflict = False

        for organism in self.organism_l:
            current_organism = self._get_organism_at(organism.x, organism.y)

            if current_organism:
                initial_conflict = True
                # two organisms occupy one element, one of them must die (chosen randomly)
                # aka choose randomly organism which will live
                organism = self.rules_engine.evolve_organism_randomly(organism,
                                                                      current_organism)
            self._populate_organism(organism)

        # in case of initial conflict - update organisms (use without conflict or with solved one)
        if initial_conflict:
            self.organism_l = self._get_all_organisms()

        return initial_conflict

    def iterate(self):
        """Main method to iterate the world.

        Public method which have to be called after the world is populated with organisms.

        Raises:
            WorldInternalError: If some of the organisms are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        evolved_organism_l = []

        for x in xrange(self.width):
            for y in xrange(self.height):
                evolved_organism = self._evolve_organism_at(x, y)
                if evolved_organism:
                    evolved_organism_l.append(evolved_organism)

        if evolved_organism_l:
            self.organism_l = evolved_organism_l
            # rebuild the grid and set it with evolved organisms
            self._repopulate_organisms(self.organism_l)

    def _evolve_organism_at(self, x, y):
        """Evolves organism at coordinates x|y.

        Evolution happens by applying all the rules specified in the evolution engine.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            organism (Organism): Organism if evolved, else None.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        evolved_organism = None
        organism = self._get_organism_at(x, y)
        neighboring_organism_l = self._get_neighboring_organisms_at(x, y)

        try:
            evolved_organism = self.rules_engine.evolve_organism_by_all_rules(
                organism, neighboring_organism_l, cell=(x, y))
        except EngineCanNotEvolveOrganismError as err:
            # could not evolve organism (this element will not go to the other iteration)
            pass
        finally:
            return evolved_organism

    def _repopulate_organisms(self, organism_l):
        """Repopulates the world with new generation of organisms. (evolved ones)

        Mainly rebuilds the grid and populate organisms to it.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        self.world_grid.rebuild()
        self._populate_organisms(organism_l)   

    def _populate_organisms(self, organism_l):
        """Populates organisms to the grid.

        Attributes:
            organism_l (list): Organisms to be populated to the grid.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        try:
            self.world_grid.set_organisms(organism_l)
        except WorldGridCoordinatesError as err:
            # we can not continue with this error (WorldInternalError)
            raise WorldInternalError('Organisms (x|y) can not be set. %s' % err.message)

    def _populate_organism(self, organism):
        """Populates organism to the grid.

        Attributes:
            organism (Organism): Organism to be populated to the grid.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid.
        """
        try:
            self.world_grid.set_organism(organism)
        except WorldGridCoordinatesError as err:
            # we can not continue with this error (WorldInternalError)
            raise WorldInternalError('Organism (x|y) can not be set. %s' % err.message)
        
    def _get_neighboring_organisms_at(self, x, y):
        """Retrieves neighbouring organisms at coordinates x|y.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            neighboring_organism_l (list): Organisms surrounding coordinates (x|y).

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        neighboring_cell_l = self._get_neighbours_space(x, y)
        neighboring_organism_l = self._get_organisms_at(neighboring_cell_l)

        return neighboring_organism_l

    def _get_organisms_at(self, cell_l):
        """Retrieves organisms at cells x|y.

        Attributes:
            cell_l (list): Cells defined by x|y coordinates.

        Returns:
            organism (Organism): Organism if exist, else None.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        organism_l = []

        for cell in cell_l:
            organism = self._get_organism_at(cell[0], cell[1])
            organism_l.append(organism) 

        return organism_l

    def _get_organism_at(self, x, y):
        """Retrieves organism at coordinates x|y.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            organism (Organism): Organism if exist, else None.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid.
        """
        try:
            return self.world_grid.get_organism_at(x, y)
        except WorldGridCoordinatesError as err:
            # we can not continue with this error (Game Internal error)
            raise WorldInternalError('Organism (X|Y) does not exist. %s' % err.message)

    def _get_neighbours_space(self, x, y):
        """Retrieves possible space for organisms in neighbourhood.

        Attributes:
            x (int): Coordinate at x axes.
            y (int): Coordinate at y axes.

        Returns:
            (list): Neihbouring cells if exist, else empy list.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            if the method `populate_initial_organisms` was called after the world's creation.
        """
        try:
            return self.world_grid.get_neighboring_cells_at(x, y)
        except WorldGridCoordinatesError as err:
            # we can not continue with this error (Game Internal error)
            raise WorldInternalError('Neighbors (X|Y) does not exist. %s' % err.message)       

    def _get_all_organisms(self):
        """Retrieves all organisms which are positioned on the grid at the moment.

        Returns:
            organism_l (list): Organisms positioned on the grid.

        Raises:
            WorldInternalError: If coordinates (x|y) are not valid. Should not happen
            unless someone change the grid (width/heigth) manually.
        """
        organism_l = []

        for x in xrange(self.width):
            for y in xrange(self.height):
                organism = self._get_organism_at(x, y)
                if organism:
                    organism_l.append(organism)

        return organism_l


class WorldInternalError(Exception):
    pass
