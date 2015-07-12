#!/usr/bin/env python
# -*-coding:utf8-*-

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager

from model import Board, Problem
from view import SudokuScreen
from view.widget import *

Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '480')

Builder.load_file('kv/sudoku.kv')


problem = Problem.loads(
            "800523910162489075350170420425008009690000"
            "057700600234037062041540317692016954003",
            "87452391616248937535917642842573816969324185"
            "7781695234937862541548317692216954783",
            9)
board = Board(problem)

sm = ScreenManager()
sm.switch_to(SudokuScreen(board_model=board))


class SudokuApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    SudokuApp().run()
