#!/usr/bin/env python
import unittest

from life_game.models.organism import Organism
from life_game.rules.evolution_rules_engine import EvolutionRulesEngine, \
    EngineCanNotEvolveOrganismError
 

class TestEvolutionRulesEngine(unittest.TestCase):
 
    def setUp(self):
        self.rules_engine = EvolutionRulesEngine()

        self.original_organism = Organism(0, 1, 1)
        self.neighboring_organism_l = [Organism(0, 2, 1), Organism(1, 2, 1), Organism(1, 1, 1)]

    def test_evolve_organism_by_all_rules_success(self):
        # we do not test all the rules again as we've already tested them in TestEvolutionRules
        organism = self.rules_engine.evolve_organism_by_all_rules(self.original_organism,
                                                                  self.neighboring_organism_l)
        self.assertEqual(organism, self.original_organism)

    def test_evolve_organism_by_all_rules_can_not_evolve(self):
        self.species_occurrence_d = {}

        with self.assertRaises(EngineCanNotEvolveOrganismError):
            self.rules_engine.evolve_organism_by_all_rules(None, self.species_occurrence_d)
