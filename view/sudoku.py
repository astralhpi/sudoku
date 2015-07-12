#!/usr/bin/env python
# -*-coding:utf8-*-

import numpy as np

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ObjectProperty, ReferenceListProperty)

from math import sqrt


class SudokuCell(Widget):
    num = NumericProperty(0)
    row = NumericProperty(0)
    col = NumericProperty(0)
    loc = ReferenceListProperty(row, col)

    @property
    def board(self):
        return self.parent.parent.parent

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.focus()

    def focus(self):
        self.board.focused_loc = self.loc


class SudokuSquareGroup(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuSquareGroup, self).__init__(**kwargs)
        self.cells = []
        for i in xrange(self.rows * self.cols):
            cell = SudokuCell()
            self.add_widget(cell)
            self.cells.append(cell)


class NumberLayer(Widget):
    '''
    숫자들이 올라가는 레이어
    '''


class FocusLayer(Widget):
    '''
    각 포커스들이 올라가는 레이어
    '''


class GridLayer(GridLayout):
    '''
    Grid를 활용하여 위치를 지정하는 레이어
    '''
    grid_size = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(GridLayer, self).__init__(*args, **kwargs)
        self.groups = None
        self.cells = None

    def on_grid_size(self, instance, size):
        self.clear_widgets()

        sqrt_size = int(sqrt(size))
        self.rows, self.cols = sqrt_size, sqrt_size

        self.groups = np.ndarray((size, size), dtype=object)
        self.cells = np.ndarray((size, size), dtype=object)

        for i in xrange(size):
            group = SudokuSquareGroup(
                rows=sqrt_size, cols=sqrt_size)
            self.add_widget(group)

            cells = group.cells
            for j in xrange(size):
                self.groups[i][j] = cells[j]

        for group_idx, group in enumerate(self.groups):
            for cell_idx, cell in enumerate(group):
                group_pos = np.asarray(
                    (group_idx / 3, group_idx % 3), dtype=int)
                cell_pos = np.asarray((cell_idx / 3, cell_idx % 3), dtype=int)
                pos = group_pos * 3 + cell_pos
                row, col = pos

                self.cells[row, col] = cell
                cell.row = int(row)
                cell.col = int(col)


class SudokuBoard(Widget):
    grid_layer = ObjectProperty()
    focus_layer = ObjectProperty()
    number_layer = ObjectProperty()

    board_model = ObjectProperty()

    focused_row = NumericProperty(0)
    focused_col = NumericProperty(0)
    focused_loc = ReferenceListProperty(focused_row, focused_col)

    def on_board_model(self, instance, board):
        self.grid_layer.clear_widgets()
        self.number_layer.clear_widgets()

        size = board.size
        self.grid_layer.grid_size = size
        self.focused_loc = (size/2, size/2)

        for i in range(size):
            for j in range(size):
                self.grid_layer.cells[i][j].num = int(board.problem[i][j])


class SudokuScreen(Screen):
    playtime = NumericProperty(0.0)
    board = ObjectProperty()

    def __init__(self, board_model, **kwargs):
        super(SudokuScreen, self).__init__(**kwargs)
        self.board.board_model = board_model

    def on_enter(self):
        Clock.schedule_interval(self.update_playtime, 0.2)

    def on_pre_leave(self):
        Clock.unschedule(self.update_playtime)

    def update_playtime(self, dt):
        self.playtime += dt
