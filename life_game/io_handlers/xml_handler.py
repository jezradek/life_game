#!/usr/bin/env python
from lxml import etree

from life_game.models.state import State
from life_game.models.organism import Organism


class XMLHandlerMixin(object):
    """Provides methods to operate with XML files.

    Has a dependency on the `lxml` module.
    """
    ELEMENT_START = 'start'
    ELEMENT_END = 'end'

    ELEMENT_LIFE = 'life'
    ELEMENT_WORLD = 'world'
    ELEMENT_CELLS = 'cells'
    ELEMENT_SPECIES = 'species'
    ELEMENT_ITERATIONS = 'iterations'
    ELEMENT_ORGANISMS = 'organisms'
    ELEMENT_ORGANISM = 'organism'
    ELEMENT_X_POS = 'x_pos'
    ELEMENT_Y_POS = 'y_pos'

    def read_state_from_xml(self, input_file):
        """Reads a state from specified XML file.

        Uses a `iterparse` which is more efficient with memory.

        Attributes:
            input_file (str): Path to the input XML file.

        Returns:
            state (State): Parsed state from input XML file.

        Raises:
            XMLFileError: If XML file is not valid or state can not be read from the file.
        """
        state_xml = etree.iterparse(input_file, events=(self.ELEMENT_START, self.ELEMENT_END))

        cells_cnt, species_cnt, iterations_cnt = None, None, None
        organism_l = []

        # the file is very small - it is not necessary to clear the elements
        try:
            for event, element in state_xml:
                if event == self.ELEMENT_END:
                    if element.tag == self.ELEMENT_WORLD:
                        cells_cnt, species_cnt, iterations_cnt = self._read_element_world(element)
                    elif element.tag == self.ELEMENT_ORGANISM:
                        organism = self._read_element_organism(element)
                        organism_l.append(organism)
        except etree.XMLSyntaxError as err:
            raise XMLFileError('XML must be valid: %s' % err.message)
        except TypeError as err:
            raise XMLFileError('Predefined XML elements must have a value: %s' % err.message)

        return State(cells_cnt, species_cnt, iterations_cnt, organism_l)

    def write_state_to_xml(self, output_file, state, iteration):
        """Writes a state and current iteration into the output file.

        Note:
             Output file is kept open as the IO operations are quite expensive.

        Attributes:
            output_file (File): Opened output file.
            state (State): State to be written in the output file.
            iteration (int): Iteration to be written in the output file.

        Raises:
            XMLFileError: If state can not be written to the output file.
        """
        life = etree.Element(self.ELEMENT_LIFE)

        world = self._write_world_element(state, iteration)
        life.append(world)

        organisms = self._write_organisms_element(state.organism_l)
        life.append(organisms)

        xml_life = etree.ElementTree(life)

        try:
            xml_life.write(output_file, xml_declaration=True, encoding='utf-8', pretty_print=True)
        except (OSError, IOError) as err:
            raise XMLFileError('Can not write to the XML file. %s' % err.message)

    def _read_element_world(self, world):
        """Parses the element world.

        Attributes:
            world (etree.Element): XML element world.

        Returns:
            cells_cnt (int): Number of cells.
            species_cnt (int): Number of species.
            iterations_cnt (int): Number of iterations.
        """
        cells_cnt, species_cnt, iterations_cnt = None, None, None

        for child in world:
            if child.tag == self.ELEMENT_CELLS:
                cells_cnt = child.text
            elif child.tag == self.ELEMENT_SPECIES:
                species_cnt = child.text
            elif child.tag == self.ELEMENT_ITERATIONS:
                iterations_cnt = child.text

        return int(cells_cnt), int(species_cnt), int(iterations_cnt)

    def _read_element_organism(self, organism):
        """Parses the element organism.

        Attributes:
            organism (etree.Element): XML element organism.

        Returns:
            organism (Organism): Parsed Organism.
        """
        x, y, species = None, None, None

        for child in organism:
            if child.tag == self.ELEMENT_X_POS:
                x = child.text
            elif child.tag == self.ELEMENT_Y_POS:
                y = child.text
            elif child.tag == self.ELEMENT_SPECIES:
                species = child.text

        return Organism(int(x), int(y), int(species))

    def _write_world_element(self, state, iteration):
        """Creates the element world.

        Attributes:
            state (State): State to be serialized to XML.
            iteration (int): Iteration to be serialized to XML.

        Returns:
            world (etree.Element): XML element world.
        """
        world = etree.Element(self.ELEMENT_WORLD)

        cells = etree.Element(self.ELEMENT_CELLS)
        cells.text = str(state.cells_cnt)
        world.append(cells)

        species = etree.Element(self.ELEMENT_SPECIES)
        species.text = str(state.species_cnt)
        world.append(species)

        iterations = etree.Element(self.ELEMENT_ITERATIONS)
        iterations.text = str(iteration)
        world.append(iterations)

        return world

    def _write_organisms_element(self, organism_l):
        """Creates the element organisms.

        Attributes:
            organism_l (list): Organisms to be serialized to XML.

        Returns:
            organism (etree.Element): XML element organism.
        """
        organisms = etree.Element(self.ELEMENT_ORGANISMS)

        for organism in organism_l:
            organism_element = etree.Element(self.ELEMENT_ORGANISM)

            x_pos = etree.Element(self.ELEMENT_X_POS)
            x_pos.text = str(organism.x)
            organism_element.append(x_pos)

            y_pos = etree.Element(self.ELEMENT_Y_POS)
            y_pos.text = str(organism.y)
            organism_element.append(y_pos)

            species = etree.Element(self.ELEMENT_SPECIES)
            species.text = str(organism.species)
            organism_element.append(species)

            organisms.append(organism_element)

        return organisms


class XMLFileError(Exception):
    pass
