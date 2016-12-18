import string
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ListProperty
from kivy.uix.widget import Widget

from kivy.core.window import Window


class LettersWidget(Widget):
    letter = StringProperty()
    score = StringProperty()
    score_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.get_letter()

    def get_letter(self, *args):
        self.ids.letter.color = self.random_color
        self.letter = random.choice(string.ascii_uppercase)
        self.play_sound(self.letter)

    def check_input(self, key):
        self.set_letter_alpha(0.4)
        if key.upper() == self.letter:
            self.score = 'OK'
            self.score_color = self.ok_color
            self.play_sound('Ok')
            Clock.schedule_once(self.get_letter, 1)
        else:
            self.score = 'WRONG'
            self.play_sound('Uh_oh')
            self.score_color = self.wrong_color
        Clock.schedule_once(self.clear_score, 1)

    def set_letter_alpha(self, alpha):
        letter_color = self.ids.letter.color
        letter_color[3] = alpha
        self.ids.letter.color = letter_color

    def clear_score(self, *args):
        self.score = ''
        self.set_letter_alpha(1)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] in string.ascii_letters:
            self.check_input(keycode[1])

    def play_sound(self, sound_file=None):
        sound = SoundLoader.load('audio/ogg/{}.ogg'.format(sound_file))
        if sound:
            sound.play()

    @property
    def random_color(self):
        r = random.random()
        g = random.random()
        b = random.random()
        return (r, g, b, 1)

    @property
    def ok_color(self):
        return (0, 1, 0, 1)

    @property
    def wrong_color(self):
        return (1, 0, 0, 1)


class LettersApp(App):

    def build(self):
        return LettersWidget()


if __name__ == '__main__':
    LettersApp().run()
