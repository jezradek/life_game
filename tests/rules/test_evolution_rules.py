#!/usr/bin/env python
import unittest

from life_game.models.organism import Organism
from life_game.rules.evolution_rules import EvolutionSurvivalRule, EvolutionIsolationRule, \
    EvolutionOvercrowdingRule, EvolutionBirthRule, EvolutionRuleError


class TestEvolutionRules(unittest.TestCase):
 
    def setUp(self):
        self.species_occurrence_d = {1 : 2, 2 : 3, 3 : 1, 4 : 4, 5 : 6}
        self.original_organism = Organism(0, 1, 1)

        self.survival_rule = EvolutionSurvivalRule()
        self.isolation_rule = EvolutionIsolationRule()
        self.overcrowding_rule = EvolutionOvercrowdingRule()
        self.birth_rule = EvolutionBirthRule()

    def test_survival_rule_applied_success(self):
        # check for two neighbours
        organism, applied = self.survival_rule.apply(self.original_organism,
                                                     self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertTrue(applied)

        # change species 
        self.original_organism.species = 2
        # check for three neighbours
        organism, applied = self.survival_rule.apply(self.original_organism,
                                                     self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertTrue(applied)        

    def test_survival_rule_not_applied_too_many_neigbours(self):
        self.species_occurrence_d = {1: 10}
        organism, applied = self.survival_rule.apply(self.original_organism,
                                                     self.species_occurrence_d)
        self.assertEqual(organism, None)
        self.assertFalse(applied)

    def test_survival_rule_not_applied_no_neigbours(self):
        self.species_occurrence_d = {}
        organism, applied = self.survival_rule.apply(self.original_organism,
                                                     self.species_occurrence_d)
        self.assertEqual(organism, None)
        self.assertFalse(applied)

    def test_survival_rule_not_applicable(self):
        # not applicable for organism which does not exist
        with self.assertRaises(EvolutionRuleError):
            organism, applied = self.survival_rule.apply(None, self.species_occurrence_d)

    def test_starvation_rule_applied_success(self):
        self.original_organism.species = 3
        # check for 1 neighbours
        organism, applied = self.isolation_rule.apply(self.original_organism,
                                                      self.species_occurrence_d)
        self.assertEqual(organism, None)
        self.assertTrue(applied)

    def test_starvation_rule_not_applied_too_many_neigbours(self):
        self.original_organism.species = 4
        organism, applied = self.isolation_rule.apply(self.original_organism,
                                                      self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertFalse(applied)

    def test_starvation_rule_not_applied_no_neigbours(self):
        self.species_occurrence_d = {}
        organism, applied = self.isolation_rule.apply(self.original_organism,
                                                      self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertFalse(applied)

    def test_starvation_rule_not_aplicable(self):
        # not applicable for organism which does not exist
        with self.assertRaises(EvolutionRuleError):
            organism, applied = self.survival_rule.apply(None, self.species_occurrence_d)

    def test_overcrowding_rule_applied_success(self):
        self.original_organism.species = 5
        # check for 6 neighbours
        organism, applied = self.overcrowding_rule.apply(self.original_organism,
                                                         self.species_occurrence_d)
        self.assertEqual(organism, None)
        self.assertTrue(applied)

    def test_starvation_rule_not_applied_too_few_neigbours(self):
        organism, applied = self.overcrowding_rule.apply(self.original_organism,
                                                         self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertFalse(applied)

    def test_starvation_rule_not_applied_no_neigbours(self):
        self.species_occurrence_d = {}
        organism, applied = self.overcrowding_rule.apply(self.original_organism,
                                                         self.species_occurrence_d)
        self.assertEqual(organism, self.original_organism)
        self.assertFalse(applied)

    def test_birth_rule_not_aplicable(self):
        # not applicable for organism which does not exist
        with self.assertRaises(EvolutionRuleError):
            organism, applied = self.overcrowding_rule.apply(None, self.species_occurrence_d)

    def test_birth_rule_applied_success(self):
        self.original_organism.species = 2
        # check for three neighbours
        organism, applied = self.birth_rule.apply(None, self.species_occurrence_d, cell=(1, 1))
        self.assertEqual(organism.species, self.original_organism.species)
        self.assertTrue(applied)        

    def test_birth_rule_not_applied_too_many_neigbours(self):
        self.species_occurrence_d = {5 : 6}
        organism, applied = self.birth_rule.apply(None, self.species_occurrence_d, cell=(1, 1))
        self.assertEqual(organism, None)
        self.assertFalse(applied)

    def test_birth_rule_not_applied_no_neigbours(self):
        self.species_occurrence_d = {}
        organism, applied = self.birth_rule.apply(None, self.species_occurrence_d, cell=(1, 1))
        self.assertEqual(organism, None)
        self.assertFalse(applied)

    def test_birth_rule_not_applicable(self):
        # not applicable for organism which does not exist
        with self.assertRaises(EvolutionRuleError):
            organism, applied = self.birth_rule.apply(self.original_organism,
                                                      self.species_occurrence_d,
                                                      cell=(1, 1))
