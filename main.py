#!/usr/bin/env python
# -*-coding:utf8-*-
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import NumericProperty
from datetime import timedelta

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


class InGameScreen(Screen):
    playtime = NumericProperty(0.0)

    def on_enter(self):
        Clock.schedule_interval(self.update_playtime, 0.2)

    def on_pre_leave(self):
        Clock.unschedule(self.update_playtime)

    def update_playtime(self, dt):
        self.playtime += dt


sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(NewGameScreen(name='newgame'))
sm.add_widget(InGameScreen(name='ingame'))
sm.current = 'ingame'


class SudokuApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    SudokuApp().run()
