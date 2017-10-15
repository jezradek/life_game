#!/usr/bin/env python
from life_game.rules.utils import get_occurence_dict_by_attr
from life_game.rules.base import EvolutionRule, EvolutionRuleError
from life_game.rules.evolution_rules import EvolutionSurvivalRule, EvolutionIsolationRule, \
    EvolutionOvercrowdingRule, EvolutionBirthRule


class EvolutionRulesEngine(object):
    """Represents the evolution rules engine for the game.

    Applies predefined rules on organisms in the game.

    Attributes:
        evolution_rule_l (EvolutionRule): Rules which will be applied by engine.
    """
    def __init__(self, evolution_rule_l=[]):
        self.evolution_rule_l = evolution_rule_l

        if not self.evolution_rule_l:
            self._init_all_evolution_rules()

    def _init_all_evolution_rules(self):
        """Initializes all rules, if none were provided."""
        self.evolution_rule_l = [
            EvolutionSurvivalRule(), 
            EvolutionIsolationRule(),
            EvolutionOvercrowdingRule(),
            EvolutionBirthRule()
        ]

    def evolve_organism_by_all_rules(self, organism, neighboring_organism_l, cell=()):
        """Applies all the rules on provided organism.

        The rules are applied on the organism one by one (same as were specified).

        Attributes:
            organism (Organism): Organism on which the rules will be applied.
            species_occurrence_d (dict): Occurrence dict indicating occurrence
                of species among organisms.
            **kwargs: Keyword arguments are not used for this rule.

        Returns:
            organism (Organism): Evolved organism which will go to other iteration.

        Raises:
            EngineCanNotEvolveOrganismError: If none of the rules were applied.
        """
        species_occurrence_d = get_occurence_dict_by_attr(neighboring_organism_l, 'species')

        for evolution_rule in self.evolution_rule_l:
            try: 
                evolved_organism, applied = evolution_rule.apply(organism, 
                                                                 species_occurrence_d,
                                                                 cell=cell)
            except EvolutionRuleError as err:
                # all the rules have to be checked
                continue
            else:
                if evolved_organism and applied:
                    return evolved_organism

        raise EngineCanNotEvolveOrganismError('Organism can not be evolved by any of the rules.')

    def evolve_organism_randomly(self, organism1, organism2):
        """Selects randomly one among two organisms.

        Applying the rule: `If two organisms occupy one element, one of them must
        die (chosen randomly) (only to resolve initial conflicts).`

        Attributes:
            organism1 (Organism): Organism1 picked for selection.
            organism2 (Organism): Organism2 picked for selection.

        Returns:
            organism (Organism): selected organism.
        """
        return EvolutionRule.select_randomly(organism1, organism2)


class EngineCanNotEvolveOrganismError(Exception):
    pass
