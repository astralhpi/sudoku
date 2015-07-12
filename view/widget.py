# -*-coding:utf8-*-

from kivy.uix.label import Label
from kivy.properties import NumericProperty


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
