#!/usr/bin/env python
import sys

from life_game.models.game import Game, GameRuntimeError
from life_game.io_handlers.game_io_handler import GameIOHandler, \
    IOValidationError, ReadStateError

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def stop_with_error(error):
    """Stops the game with error status and message."""
    print GameIOHandler.usage(error.message)
    sys.exit(EXIT_FAILURE)


def stop_with_success():
    """Stops the game with success status and message."""
    print '* The game has successfully finished.'
    sys.exit(EXIT_SUCCESS)


if __name__ == '__main__':
    """Main method to run the game of life.

    Example:
    Second argument is a XML file which contains the initial state for the game.

        $ python run.py /path/to/input_file.xml

    """
    print '* The game has started. \n'

    print '* Checking the input provided. \n'
    try:
        input_file = GameIOHandler.check_input(sys.argv)
        io_handler = GameIOHandler(input_file)
    except IOValidationError as err:
        stop_with_error(err)

    print '* Reading a state from the input file. \n'
    try:
        initial_state = io_handler.read_state()
    except ReadStateError as err:
        stop_with_error(err)

    print '* Initializing the game. \n'
    game = Game(io_handler, initial_state)

    print '* Starting the game. \n'
    try:
        game.start()
    except GameRuntimeError as err:
        stop_with_error(err)
    else:
        stop_with_success()
