#!/usr/bin/env python
import random


class EvolutionRule(object):
    """Base class for evolution rules.

    Each specific rule must inherit from this class and override the `apply` method.
    """
    def apply(self, organism, species_occurrence_d, **kwargs):
        """This method must be overriden in subclass.

        Attributes:
            organism (Organism): Organism which are to be set to the grid.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments if specified.

        Raises:
            NotImplementedError: If method is not overriden.
        """
        raise NotImplementedError('This method must be overriden in subclass!')

    @staticmethod
    def select_randomly(organism1, organism2):
        """Selects randomly one among two organisms.

        Mainly for the rule: `If two organisms occupy one element, one of them must
        die (chosen randomly) (only to resolve initial conflicts).`

        Attributes:
            organism1 (Organism): Organism1 picked for selection.
            organism2 (Organism): Organism2 picked for selection.

        Returns:
            organism (Organism): selected organism.
        """
        return random.choice((organism1, organism2))


class EvolutionRuleError(Exception):
    pass
