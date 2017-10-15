#!/usr/bin/env python
from life_game.models.state import State
from life_game.models.world import World, WorldInternalError
from life_game.models.world_grid import WorldGrid
from life_game.rules.evolution_rules_engine import EvolutionRulesEngine
from life_game.io_handlers.game_io_handler import WriteStateError


class Game(object):
    """Encapsulates the whole game.

    The `start` method must be executed int order to launch the game.

    Attributes:
        io_handler (GameIOHandler): Object which handles game's IO operations.
        state (State): Current state of the Game.
    """
    def __init__(self, io_handler, state):
        self.io_handler = io_handler
        self.state = state

    def start(self):
        """Main method which starts the whole game.

        The method prepares all the necessary objects like game engine, world and world grid.
        Also proceeds with the iterations. The number of iterations is specified in the state.
        """
        print '* Initiating the rules engine. \n'
        rules_engine = EvolutionRulesEngine()

        print '* Preparing the world grid. \n'
        world_grid = WorldGrid(self.state.cells_cnt, self.state.cells_cnt)

        print '* Preparing the world itself. \n'
        world = World(world_grid, self.state.organism_l, rules_engine)
        try:
            world.populate_initial_organisms()
        except WorldInternalError as err:
            raise GameRuntimeError('Game could not be initialized: %s' % err.message)

        print '* Proceeding with iterations. \n'      
        for i in xrange(self.state.iterations_cnt, 0, -1):
            try:
                world.iterate()
            except WorldInternalError as err:
                raise GameRuntimeError('Game could not proceed with iteration: %s' % err.message)
            else:
                # save current state of the game and current iteration
                self._save(world.organism_l, i - 1)

        print '* Cleaning after iterations. \n'
        self._clean()

    def _save(self, organism_l, iteration):
        """Saves the current state of the game to the output file.

        Args:
            organism_l (list): Organisms to be saved.
            iteration (int): Iteration to be saved.
        """
        self.state = self._get_current_state(organism_l, iteration)

        try:
            self.io_handler.write_state(self.state, iteration)
        except WriteStateError as err:
            raise GameRuntimeError('Game could not save the state: %s' % err.message)

    def _get_current_state(self, organism_l, iteration):
        """Finds out the current state of the game.

        Args:
            organism_l (list): Organisms to be used in current state.
            iteration (int): Iteration to be saved in current state.

        Returns:
            State: Current state of the game.
        """
        return State(self.state.cells_cnt, self.state.species_cnt, iteration, organism_l)

    def _clean(self):
        """Cleans up after the iterations are completed.

        Mainly to clean the IO handler (close the output file).
        """
        self.io_handler.clean()


class GameRuntimeError(Exception):
    pass
