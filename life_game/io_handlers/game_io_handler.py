#!/usr/bin/env python
import os

from life_game.io_handlers.xml_handler import XMLHandlerMixin, XMLFileError


class GameIOHandler(XMLHandlerMixin):
    """Handles IO operations inside the game.

    Attributes:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
        keep_out_file_open (bool): True if output file is kept open between iterations,
            False otherwise.
    """
    def __init__(self, input_file, output_file='out.xml', keep_out_file_open=True):
        self.input_file = input_file
        self.output_file = output_file
        # in case of adding simple mode (without having the file open between iterations)
        self.keep_out_file_open = keep_out_file_open

        # we don't want to open and close file after the each iteration (its quite expensive)
        # usually better to use with statement, yet for this case
        # we want to catch and display the errors to the user
        if self.keep_out_file_open:
            self.opened_output_file = self._open_file()

    @staticmethod
    def check_input(arguments):
        """Checks the input provided by user.

        Attributes:
            arguments (list): Arguments provided to the game.

        Returns:
            input_file (str): Path to input file.

        Raises:
            IOValidationError: If the input is not specified or does not exist or
            is not a XML file (simple check).
        """
        # no need to use AgreementParser since we can encapsulate the logic here
        if len(arguments) != 2:
            raise IOValidationError('The input file must be specified.')

        input_file = arguments[1]

        if not os.path.exists(input_file):
            raise IOValidationError('The input file must exist.')

        # dummy check for xml file
        if '.xml' not in input_file:
            raise IOValidationError('The input file must be a XML file.')

        return input_file

    @staticmethod
    def usage(info=None):
        """Builds a user message (how the game should be used).

        Attributes:
            info (str, optional): Information which can be added to the user message.

        Returns:
            (str): Message about usage of the game.
        """
        note = info if info else 'The input XML file must be specified.'

        return '! Execute: <python run.py input_file.xml> in order to run the game.\n' \
               '! Error: %(note)s' % {'note' : note}

    def read_state(self, input_file=None):
        """Reads a state from the input file.

        Attributes:
            input_file (str, optional): Path to the input file.

        Returns:
            state (State): Parsed state from the input file.

        Raises:
            ReadStateError: If state can not be read from the input file or if the state
            is not valid.
        """
        if not input_file:
            input_file = self.input_file

        try:
            state = self.read_state_from_xml(input_file)
        except XMLFileError as err:
            raise ReadStateError('State can not be read from file: %s' % err.message)
        else:
            if state.is_valid():
                return state
            raise ReadStateError('State is not valid: %s' % state)

    def write_state(self, state, iteration):
        """Writes a state and current iteration into the output file.

        Note:
             Output file is kept open as the IO operations are quite expensive.

        Attributes:
            state (State): State to be written in the output file.
            iteration (int): Iteration to be written in the output file.

        Raises:
            WriteStateError: If state can not be written to the output file.
        """
        self._rewind_file()

        try:
            self.write_state_to_xml(self.opened_output_file, state, iteration)
        except XMLFileError as err:
            raise WriteStateError('State can not be written to file: %s' % err.message)

    def clean(self):
        """Mainly closes the file which is kept open between iterations."""
        self.opened_output_file.close()

    def _open_file(self):
        """Opens the output file.

        Returns:
            opened_file (File): Opened output file.

        Raises:
            IOValidationError: If the output file can not be opened.
        """
        return open(self.output_file, 'w')
        try:
            opened_file = open(self.output_file, 'w')
        except (OSError, IOError) as err:
            raise IOValidationError('Can not open the output file.')
        else:
            return opened_file

    def _rewind_file(self):
        """Rewinds the output file to the beginning.

        Since the output file is kept open, the states have to be replaced inside the file.
        """
        self.opened_output_file.seek(0)
        self.opened_output_file.truncate()


class IOValidationError(Exception):
    pass


class ReadStateError(Exception):
    pass


class WriteStateError(Exception):
    pass 
