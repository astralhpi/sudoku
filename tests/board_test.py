#!/usr/bin/env python
# -*-coding:utf8-*-

import unittest

import board


class BoardTestCase(unittest.TestCase):
    def test_load(self):
        p = '3608100705010000000080060000196080008000'\
            '40009000902480000700500000000702050021048'
        s = '3628159745914738267482961354196382578251'\
            '47369673952481284769513136584792957321648'

        problem = board.Problem.loads(p, s, 9)

        self.assertEqual(problem.problem[8, 8], 8)
        self.assertEqual(problem.problem[8, 6], 0)
        self.assertEqual(problem.solution[8, 8], 8)
        self.assertEqual(problem.solution[8, 6], 6)

        b = board.Board(problem)
        self.assertEqual(problem.size, b.size)

        b.setmemo((1, 4), 5, True)
        self.assertEqual(b.memo[1, 4, 5], True)

        b.setinput((1, 4), 5)
        self.assertEqual(b.input[1, 4], 5)

        self.assertEqual(b[1, 2], b[1, 2])

        cell = b[1, 2]
        b.setinput((1, 2), 3)
        self.assertNotEqual(cell, b[1, 2])
