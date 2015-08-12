#!/usr/bin/env python
# -*-coding:utf8-*-

import numpy as np

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (
    NumericProperty, ObjectProperty, ReferenceListProperty)

from math import sqrt


class GridCell(FloatLayout):
    row = NumericProperty(0)
    col = NumericProperty(0)
    loc = ReferenceListProperty(row, col)

    @property
    def board(self):
        return self.layer.parent

    @property
    def layer(self):
        return self.subregion.parent

    @property
    def subregion(self):
        return self.parent

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.focus()

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.focus()

    def focus(self):
        self.board.focused_loc = self.loc


class NumberCell(FloatLayout):
    num = NumericProperty(0)
    grid_cell = ObjectProperty()

    @property
    def loc(self):
        return self.grid_cell.loc


class Subregion(GridLayout):
    def __init__(self, **kwargs):
        super(Subregion, self).__init__(**kwargs)
        self.cells = []
        for i in xrange(self.rows * self.cols):
            cell = GridCell()
            self.add_widget(cell)
            self.cells.append(cell)


class NumberLayer(FloatLayout):
    '''
    숫자들이 올라가는 레이어
    '''

    def __init__(self, *args, **kwargs):
        super(NumberLayer, self).__init__(*args, **kwargs)
        self.subregions = None
        self.cells = None

    def prepare_layer(self, grid_layer):
        self.clear_widgets()
        size = grid_layer.grid_size

        self.subregions = np.ndarray((size, size), dtype=object)
        self.cells = np.ndarray((size, size), dtype=object)

        for i in xrange(size):
            for j in xrange(size):
                grid_cell = grid_layer.cells[i][j]
                cell = NumberCell(num=0, grid_cell=grid_cell)
                self.cells[i][j] = cell
                self.add_widget(cell)


class FocusLayer(FloatLayout):
    '''
    각 포커스들이 올라가는 레이어
    '''
    cell_focus = ObjectProperty()
    focused_grid_cell = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(FocusLayer, self).__init__(*args, **kwargs)
        self.prev_grid_cell = None

    def on_focused_grid_cell(self, instance, cell):
        cell.bind(pos=self.on_cell_pos_changed)
        if self.prev_grid_cell is not None:
            self.prev_grid_cell.unbind(pos=self.on_cell_pos_changed)
        self.cell_focus.pos = cell.pos
        self.prev_grid_cell = cell

    def on_cell_pos_changed(self, cell, pos):
        self.cell_focus.pos = pos


class GridLayer(GridLayout):
    '''
    Grid를 활용하여 위치를 지정하는 레이어
    '''
    grid_size = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(GridLayer, self).__init__(*args, **kwargs)
        self.subregions = None
        self.cells = None

    @property
    def board(self):
        return self.parent

    def on_grid_size(self, instance, size):
        self.clear_widgets()

        sqrt_size = int(sqrt(size))
        self.rows, self.cols = sqrt_size, sqrt_size

        self.subregions = np.ndarray((size, size), dtype=object)
        self.cells = np.ndarray((size, size), dtype=object)

        for i in xrange(size):
            subregion = Subregion(
                rows=sqrt_size, cols=sqrt_size)
            self.add_widget(subregion)

            cells = subregion.cells
            for j in xrange(size):
                self.subregions[i][j] = cells[j]

        for subregion_idx, subregion in enumerate(self.subregions):
            for cell_idx, cell in enumerate(subregion):
                subregion_pos = np.asarray(
                    (subregion_idx / 3, subregion_idx % 3), dtype=int)
                cell_pos = np.asarray((cell_idx / 3, cell_idx % 3), dtype=int)
                pos = subregion_pos * 3 + cell_pos
                row, col = pos

                self.cells[row, col] = cell
                cell.row = int(row)
                cell.col = int(col)


class SudokuBoard(FloatLayout):
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

        self.number_layer.prepare_layer(self.grid_layer)
        for i in range(size):
            for j in range(size):
                self.number_layer.cells[i][j].num = int(board.problem[i][j])

        self.focused_loc = (size/2, size/2)

    def on_focused_loc(self, instance, loc):
        focused_cell = self.grid_layer.cells[tuple(self.focused_loc)]
        self.focus_layer.focused_grid_cell = focused_cell


class NumpadButton(FloatLayout):
    number = NumericProperty(0)
    main_button = ObjectProperty()
    sub_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(NumpadButton, self).__init__(**kwargs)
        Clock.schedule_once(self.__init_widgets, -1)

    def __init_widgets(self, dt=0):
        # self.main_button.bind(on_press=)



class UpperNumpadButton(NumpadButton):
    pass


class LowerNumpadButton(NumpadButton):
    pass


class Numpad(FloatLayout):
    upper_box = ObjectProperty()
    lower_box = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(Numpad, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_widgets, -1)

    def init_widgets(self, dt=0):
        for i in range(1, 6):
            button = UpperNumpadButton(number=i)
            self.upper_box.add_widget(button)

        for i in range(6, 10):
            button = LowerNumpadButton(number=i)
            self.lower_box.add_widget(button)


class SudokuScreen(Screen):
    playtime = NumericProperty(0.0)

    board = ObjectProperty()
    numpad = ObjectProperty()

    def __init__(self, board_model, **kwargs):
        super(SudokuScreen, self).__init__(**kwargs)
        self.board.board_model = board_model

    def on_enter(self):
        Clock.schedule_interval(self.update_playtime, 0.2)

    def on_pre_leave(self):
        Clock.unschedule(self.update_playtime)

    def update_playtime(self, dt):
        self.playtime += dt
