#!/usr/bin/env python
# -*-coding:utf8-*-

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class OutGameUiScreen(Screen):
    copyright = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(OutGameUiScreen, self).__init__(*args, **kwargs)
