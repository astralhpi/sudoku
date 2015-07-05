#!/usr/bin/env python
# -*-coding:utf8-*-

import unittest
import board

import numpy as np


class BoardTestCase(unittest.TestCase):
    def setUp(self):
        p = '3608100705010000000080060000196080008000'\
            '40009000902480000700500000000702050021048'
        s = '3628159745914738267482961354196382578251'\
            '47369673952481284769513136584792957321648'

        self.problem = board.Problem.loads(p, s, 9)
        self.board = board.Board(self.problem)

    def test_load(self):

        self.assertEqual(self.problem.problem[8, 8], 8)
        self.assertEqual(self.problem.problem[8, 6], 0)
        self.assertEqual(self.problem.solution[8, 8], 8)
        self.assertEqual(self.problem.solution[8, 6], 6)

        self.assertEqual(self.problem.size, self.board.size)

    def test_memo(self):
        self.board.setmemo((1, 4), 5, True)
        self.assertEqual(self.board.memo[1, 4, 5], True)

    def test_input(self):
        self.board.setinput((1, 4), 5)
        self.assertEqual(self.board.input[1, 4], 5)

    def test_cell(self):
        self.assertEqual(self.board[1, 2], self.board[1, 2])

        cell = self.board[1, 2]
        self.board.setinput((1, 2), 3)
        self.assertNotEqual(cell, self.board[1, 2])

        self.assertEqual(self.board[0, 0].type, 'fixed')
        self.assertEqual(self.board[0, 2].type, 'empty')
        self.board.setmemo((0, 2), 3, True)
        self.assertEqual(self.board[0, 2].type, 'memo')
        self.board.setinput((0, 2), 3)
        self.assertEqual(self.board[0, 2].type, 'inputed')

        self.assertFalse(self.board[0, 2].iscorrect)
        self.board.setinput((0, 2), 3)
        self.assertFalse(self.board[0, 2].iscorrect)
        self.board.setinput((0, 2), 2)
        self.assertTrue(self.board[0, 2].iscorrect)

    def test_solved(self):
        self.assertFalse(self.board.issolved)

        it = np.nditer(self.board.solution, flags=['multi_index'])
        while not it.finished:
            i, j = it.multi_index
            self.board.setinput((i, j), it[0])
            it.iternext()

        self.assertTrue(self.board.issolved)
