#!/usr/bin/env python
# -*-coding:utf8-*-
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import NumericProperty, ObjectProperty

from math import sqrt
from board import Board, Problem

import numpy as np

Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '480')

Builder.load_file('sudoku.kv')


class MainScreen(Screen):
    pass


class NewGameScreen(Screen):
    pass


class SecondsLabel(Label):
    seconds = NumericProperty(0.0)

    def on_seconds(self, instance, value):
        value = int(value)
        seconds = value % 60
        value /= 60
        mins = value % 60
        value /= 60
        hours = value

        if hours > 0:
            text = '%d:%02d:%02d' % (hours, mins, seconds)
        else:
            text = '%02d:%02d' % (mins, seconds)

        self.text = text


class SudokuCell(Widget):
    num = NumericProperty(0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print touch


class SudokuSquareGroup(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuSquareGroup, self).__init__(**kwargs)
        self.cells = []
        for i in xrange(self.rows * self.cols):
            cell = SudokuCell(num=i)
            self.add_widget(cell)
            self.cells.append(cell)


class SudokuBoard(GridLayout):
    board_model = ObjectProperty()

    def on_board_model(self, instance, board):
        self.clear_widgets()
        size = board.size

        sqrt_size = int(sqrt(size))
        self.rows = sqrt_size
        self.cols = sqrt_size

        self.groups = np.ndarray((size, size), dtype=object)
        self.cells = np.ndarray((size, size), dtype=object)

        for i in xrange(size):
            group = SudokuSquareGroup(
                rows=sqrt_size, cols=sqrt_size)
            self.add_widget(group)

            cells = group.cells
            for j in xrange(size):
                self.cells[i][j] = cells[j]

        for group_idx, group in enumerate(self.cells):
            for cell_idx, cell in enumerate(group):
                group_pos = np.asarray((group_idx / 3, group_idx % 3))
                cell_pos = np.asarray((cell_idx / 3, cell_idx % 3))
                pos = group_pos * 3 + cell_pos
                i, j = pos

                self.cells[i, j] = cell

        for i in range(size):
            for j in range(size):
                self.cells[i][j].num = int(board.problem[i][j])


class InGameScreen(Screen):
    playtime = NumericProperty(0.0)
    board = ObjectProperty()

    def __init__(self, board_model, **kwargs):
        super(InGameScreen, self).__init__(**kwargs)
        self.board.board_model = board_model

    def on_enter(self):
        Clock.schedule_interval(self.update_playtime, 0.2)

    def on_pre_leave(self):
        Clock.unschedule(self.update_playtime)

    def update_playtime(self, dt):
        self.playtime += dt

problem = Problem.loads(
            "800523910162489075350170420425008009690000"
            "057700600234037062041540317692016954003",
            "87452391616248937535917642842573816969324185"
            "7781695234937862541548317692216954783",
            9)
board = Board(problem)

sm = ScreenManager()
sm.switch_to(InGameScreen(board_model=board))


class SudokuApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    SudokuApp().run()
