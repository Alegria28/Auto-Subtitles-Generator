import pysubs2  # So we can work with .ass subtitles
import os  # So we can work with paths


class SubtitleASSManager:

    ass_path = os.path.abspath(os.path.dirname(__file__))
    x = 0
    y = 0

    # Constructor
    def __init__(self, font, size, color, player):
        self._font = font
        self._size = size
        self._color = color
        self._player = player

    # ------ Methods ------

    def set_position_norm(self, x_norm, y_norm):
        self.x = x_norm
        self.y = y_norm

    def generate_ass():
        pass

    # ------ Getters and setters of the class ------

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    # What we'll show when we print an object
    def __str__(self):
        return (
            f"Fuente: {self.font}\n"
            f"Tamaño: {self.size}\n"
            f"Color: {self.color}\n"
            f"Posición: ({self.x}, {self.y})"
        )
