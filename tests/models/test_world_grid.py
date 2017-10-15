#!/usr/bin/env python
import unittest

from life_game.models.world_grid import WorldGrid, WorldGridCoordinatesError
from life_game.models.organism import Organism


class TestWorldGrid(unittest.TestCase):
 
    def setUp(self):
        self.world_grid = WorldGrid(4, 4)

        self.organism = Organism(0, 2, 1)
        self.organism_wrong_x = Organism(-1, 2, 1)
        self.organism_wrong_y = Organism(1, -3, 1)
        self.organism_wrong_xy = Organism(-1, -5, 1)
        self.organism_out_x = Organism(10, 2, 1)
        self.organism_out_y = Organism(2, 20, 1)
        self.organism_out_xy = Organism(22, 20, 1)

    def test_height(self):
        self.assertEqual(self.world_grid.height, 4)
        self.assertEqual(len(self.world_grid.grid), 4)
 
    def test_width(self):
        self.assertEqual(self.world_grid.width, 4)
        self.assertEqual(len(self.world_grid.grid[0]), 4)

    def test_set_organism_success(self):
        self.world_grid.set_organism(self.organism)
        organism_at = self.world_grid.get_organism_at(0, 2)

        self.assertEqual(self.organism, organism_at)

    def test_set_organism_wrong_coordinates(self):
        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_wrong_x)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_wrong_x)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_wrong_xy)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_out_x)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_out_y)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.set_organism(self.organism_out_xy)             

    def test_get_organism_success(self):
        organism_at = self.world_grid.get_organism_at(0, 2)
        organism = self.world_grid.grid[0][2]

        self.assertEqual(organism_at, organism)

    def test_get_organism_wrong_coordinates(self):
        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(-1, 2)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(1, -3)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(-1, -4)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(10, 2)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(2, 20)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_organism_at(20, 22)                           

    def test_get_neighboring_cells_at_success(self):
        # test left up corner
        lup_corner_cell_l = self.world_grid.get_neighboring_cells_at(0, 0)
        # test right up corner
        rup_corner_cell_l = self.world_grid.get_neighboring_cells_at(3, 0)
        # test left down corner
        ldown_corner_cell_l = self.world_grid.get_neighboring_cells_at(0, 3)
        # test right down corner
        rdown_corner_cell_l = self.world_grid.get_neighboring_cells_at(3, 3)
        # test middle cell
        middle_cell_l = self.world_grid.get_neighboring_cells_at(1, 1)

        self.assertEqual(len(lup_corner_cell_l), 3)
        self.assertEqual(len(rup_corner_cell_l), 3)
        self.assertEqual(len(ldown_corner_cell_l), 3)
        self.assertEqual(len(rdown_corner_cell_l), 3)
        self.assertEqual(len(middle_cell_l), 8)

    def test_get_neighboring_cells_at_wrong_coordinates(self):
        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(-1, 2)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(1, -3)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(-1, -4)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(10, 2)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(2, 20)

        with self.assertRaises(WorldGridCoordinatesError):
            self.world_grid.get_neighboring_cells_at(20, 22)
