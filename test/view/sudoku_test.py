# -*-coding:utf8-*-

import main
import unittest

from kivy.config import Config
from model.sudoku import Problem, Board
from view.sudoku import SudokuBoard


class SudokuBoardTest(unittest.TestCase):
    def setUp(self):
        Config.set('kivy', 'log_level', 'warning')
        self.problem = Problem.loads(
            "800523910162489075350170420425008009690000"
            "057700600234037062041540317692016954003",
            "87452391616248937535917642842573816969324185"
            "7781695234937862541548317692216954783",
            9)
        self.board = Board(self.problem)

        self.board_view = SudokuBoard()
        self.board_view.board_model = self.board

    def test_initialize(self):
        for i in xrange(self.board.size):
            for j in xrange(self.board.size):
                cell = self.board_view.number_layer.cells[i][j]
                self.assertEqual(
                    cell.num,
                    self.board.problem[i][j],
                    'GUI 숫자와 문제의 숫자가 일치하는지 확인함.')
                self.assertEqual(
                    cell.loc,
                    [i, j],
                    '셀의 위치가 문제의 위치와 위치하는지 확인함')

    def test_select_cell(self):
        for i in xrange(self.board.size):
            for j in xrange(self.board.size):
                cell = self.board_view.grid_layer.cells[i][j]
                cell.focus()

                self.assertEqual(
                    self.board_view.focused_loc,
                    [i, j])
