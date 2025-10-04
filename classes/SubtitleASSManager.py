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
        self.position_name = "Bottom"  # Default position

    # ------ Methods ------

    def set_position_norm(self, x_norm, y_norm):
        self.x = x_norm
        self.y = y_norm

    def hex_to_ass_color(self, hex_color):
        # Convert a hex color like #RRGGBB to the ASS format &HBBGGRR&.
        if not hex_color.startswith("#") or len(hex_color) != 7:
            return "&HFFFFFF&"  # Default to white on error
        r = hex_color[1:3]
        g = hex_color[3:5]
        b = hex_color[5:7]
        return f"&H{b.upper()}{g.upper()}{r.upper()}&"

    def generate_ass(self, text, video_size, duration):

        # Generate a preview .ass file with the current style settings
        subs = pysubs2.SSAFile()
        video_w, video_h = video_size

        # Set the script resolution to match the video resolution, this ensures that font sizes and positions are scaled correctly
        subs.info["PlayResX"] = video_w
        subs.info["PlayResY"] = video_h
        subs.info["WrapStyle"] = 1  # Smart wrapping

        # Map position names to ASS alignment values
        # (1: Bottom-Left, 2: Bottom-Center, 3: Bottom-Right, 5: Middle-Center, 8: Top-Center)
        alignment_map = {"Bottom": 2, "Middle": 5, "Top": 8}

        # Define the main style for the subtitles.
        style = pysubs2.SSAStyle()
        style.fontname = self._font
        style.fontsize = self._size
        style.primarycolor = self.hex_to_ass_color(self._color)

        # If the position is 'Custom', set alignment to Middle-Center (5) to match the final video
        if self.position_name == "Custom":
            style.alignment = 5
        # Otherwise, use the alignment map for predefined positions.
        else:
            style.alignment = alignment_map.get(self.position_name)

        subs.styles["MainStyle"] = style

        # If the position is 'Custom', use position tags
        if self.position_name == "Custom":
            # Convert normalized coordinates to absolute pixel values for the \pos(x,y) tag.
            x_px = int(self.x * video_w)
            y_px = int(self.y * video_h)
            event_text = f"{{\\pos({x_px},{y_px})}}{text}"
        # Otherwise, rely on alignment
        else:
            event_text = text

        # Create a subtitle event that lasts for the given duration
        event = pysubs2.SSAEvent(
            start=0, end=duration, text=event_text, style="MainStyle"
        )
        subs.append(event)

        # Save the .ass file and return its absolute path
        out_path = os.path.join(self.ass_path, "preview.ass")
        subs.save(out_path, encoding="utf-8")

        return out_path

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
