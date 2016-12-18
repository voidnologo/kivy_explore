import string
import random
import time

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.core.window import Window


class LettersWidget(Widget):
    letter = StringProperty()
    score = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.get_letter()

    def get_letter(self):
        self.letter = random.choice(string.ascii_uppercase)

    def check_input(self, key):
        if key.upper() == self.letter:
            self.score = 'OK'
            self.get_letter()
        else:
            self.score = 'WRONG'
        Clock.schedule_once(self.clear_score, 1)

    def clear_score(self, dt):
        self.score = ''

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.check_input(keycode[1])


class LettersApp(App):

    def build(self):
        return LettersWidget()


if __name__ == '__main__':
    LettersApp().run()
