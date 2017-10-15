#!/usr/bin/env python
import random

from life_game.models.organism import Organism
from life_game.rules.base import EvolutionRule, EvolutionRuleError


class EvolutionSurvivalRule(EvolutionRule):
    """Survival evolution rule (derived from base evolution rule).

    Definition: `If there are two or three organisms of the same type living in the elements
    surrounding an organism of the same, type then it may survive.`
    """
    def apply(self, organism, species_occurrence_d, **kwargs):
        """Overrides method derived from base class.

        Note:
        Organism will survive only if the rule was applied.

        Attributes:
            organism (Organism): Organism or (None) on which the rule will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments are not used for this rule.

        Returns:
            organism (Organism): Survived organism, None otherwise.
            applied (bool): Indicates if the rule was applied.

        Raises:
            EvolutionRuleError: If organism does not exist.
        """
        if not organism:
            raise EvolutionRuleError('Not applicable - organism must exist.')

        evolved_organism = None
        applied = False

        if species_occurrence_d:
            species_occurrence = species_occurrence_d.get(organism.species)
            if species_occurrence and species_occurrence in [2, 3]:
                # organism can survive, there are two or three neighbours
                evolved_organism = organism
                applied = True

        return evolved_organism, applied


class EvolutionIsolationRule(EvolutionRule):
    """Isolation evolution rule (derived from base evolution rule).

    Definition: `If there are less than two organisms of one type surrounding one of the same
    type then it will die due to isolation.`
    """
    def apply(self, organism, species_occurrence_d, **kwargs):
        """Overrides method derived from base class.

        Note:
        Organism will die only if the rule was applied.

        Attributes:
            organism (Organism): Organism or (None) on which the rule will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments are not used for this rule.

        Returns:
            organism (Organism): Dead organism (None), original Organism otherwise.
            applied (bool): Indicates if the rule was applied.

        Raises:
            EvolutionRuleError: If organism does not exist.
        """
        if not organism:
            raise EvolutionRuleError('Not applicable - organism must exist.')

        evolved_organism = organism
        applied = False

        if species_occurrence_d:
            species_occurrence = species_occurrence_d.get(organism.species)
            if species_occurrence and species_occurrence < 2:
                # organism will die as there is 0 or 1 neighbours
                evolved_organism = None
                applied = True

        return evolved_organism, applied


class EvolutionOvercrowdingRule(EvolutionRule):
    """Overcrowding evolution rule (derived from base evolution rule).

    Definition: `If there are four or more organisms of one type surrounding one of the same
    type then it will die due to overcrowding.`
    """
    def apply(self, organism, species_occurrence_d, **kwargs):
        """Overrides method derived from base class.

        Note:
        Organism will die only if the rule was applied.

        Attributes:
            organism (Organism): Organism or (None) on which the rule will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments are not used for this rule.

        Returns:
            organism (Organism): Dead organism (None), original Organism otherwise.
            applied (bool): Indicates if the rule was applied.

        Raises:
            EvolutionRuleError: If organism does not exist.
        """
        if not organism:
            raise EvolutionRuleError('Not applicable - organism must exist.')

        evolved_organism = organism
        applied = False

        if species_occurrence_d:
            species_occurrence = species_occurrence_d.get(organism.species)
            if species_occurrence and species_occurrence > 4:
                # organism will die as there is more than 4 neighbours
                evolved_organism = None
                applied = True

        return evolved_organism, applied


class EvolutionBirthRule(EvolutionRule):
    """Birth evolution rule (derived from base evolution rule).

    Definition: `If there are exactly three organisms of one type surrounding one element, they
    may give birth into that cell. The new organism is the same type as its parents. If this
    condition is true for more then one species on the same element then species type for the
    new element is chosen randomly.`
    """
    def apply(self, organism, species_occurrence_d, **kwargs):
        """Overrides method derived from base class.

        Note:
        Organism will be born only if the rule was applied.

        Attributes:
            organism (Organism): Organism or (None) on which the rule will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.Indicating
            **kwargs: Keyword arguments contain the cell (x|y) for organism to be born at.

        Returns:
            organism (Organism): Born organism, None otherwise.
            applied (bool): Indicates if the rule was applied.

        Raises:
            EvolutionRuleError: If organism does not exist.
        """
        if organism:
            raise EvolutionRuleError('Not applicable - organism must not exist.')

        evolved_organism = None
        applied = False
        birth_species_candidate_l = []

        if species_occurrence_d:
            for species, occurrence in species_occurrence_d.iteritems():
                if occurrence == 3:
                    birth_species_candidate_l.append(species)

        if birth_species_candidate_l:
            # if there are 3 organisms with same species, choose one and give a birth 
            random_species = random.choice(birth_species_candidate_l)
            cell = kwargs.get('cell')
            evolved_organism = Organism(cell[0], cell[1], random_species)
            applied = True

        return evolved_organism, applied
