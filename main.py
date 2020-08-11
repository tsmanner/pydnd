import curses
import enum
import json
import types
import sys
import textwrap
from world import *
from world.tui.pane import Pane



class ScrollDirection(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()


class ScrollablePane(Pane):
    def up(self):
        if self.pad_viewport_top_left[0] > 1:
            self.pad_viewport_top_left = (self.pad_viewport_top_left[0] - 1, 0)
        self.refresh()

    def down(self):
        if (self.pad_viewport_top_left[0] - 1 + self.height) < self.pad_size[0]:
            self.pad_viewport_top_left = (self.pad_viewport_top_left[0] + 1, 0)
        self.refresh()


class TextPane(ScrollablePane):
    def __init__(self, default_message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.pause_proxy():
            self.default_message = default_message

    def __call__(self, message=None):
        self.clear()
        if message is None:
            if callable(self.default_message):
                message = self.default_message()
            else:
                message = self.default_message
        if isinstance(message, str):
            self.addstr(0, 1, message)
        else:
            for i, line in enumerate(message):
                if i == (self.pad_size[0]):
                    break
                self.addstr(i, 2, line)
        self.border()
        self.refresh()


class MenuPane(ScrollablePane):
    def __init__(self, data, *args, renderer=lambda i, d: str(d), **kwargs):
        super().__init__(*args, **kwargs)
        with self.pause_proxy():
            self._selected_index = 0
            self.data = data
            self.renderer = renderer

    def set_data(self, data, renderer=None):
        self.clear()
        self.border()
        if renderer:
            self.renderer = renderer
        self.data = data
        for i, d in enumerate(self.data):
            self.addstr(i, 1, self.renderer(i, d))
        self._selected_index = 0
        self.pad_viewport_top_left = (0, 0)
        self.refresh()

    def refresh(self):
        self.move(self.selected_index, 1)
        super().refresh()

    def up(self):
        message = f"{self._selected_index} -> "
        if self._selected_index > 0:
            self._selected_index -= 1
        message += f"{self._selected_index}: {self.pad_viewport_top_left} -> "
        if self._selected_index != 0 and self._selected_index == (self.pad_viewport_top_left[0]):
            self.pad_viewport_top_left = (self.pad_viewport_top_left[0] - 1, 0)
        message += f"{self.pad_viewport_top_left}"
        self.status_pane(message)
        self.refresh()

    def down(self):
        message = f"{self._selected_index} -> "
        if self._selected_index < (len(self.data) - 1):
            self._selected_index += 1
        message += f"{self._selected_index}: {self.pad_viewport_top_left} -> "
        if self._selected_index != len(self.data) - 1 and self._selected_index == (self.pad_viewport_top_left[0] - 1 + self.height):
            self.pad_viewport_top_left = (self.pad_viewport_top_left[0] + 1, 0)
        message += f"{self.pad_viewport_top_left}"
        self.status_pane(message)
        self.refresh()

    @property
    def selected_index(self):
        return self._selected_index

    @property
    def selected(self):
        return self.data[self.selected_index]


class UI:
    def __init__(self, screen, filename):
        self.screen = screen
        json_data = json.load(open(filename))
        self.objects = from_json(json_data["objects"])
        campaign = Location(name=json_data["name"])
        for root in filter(lambda o: o.location is None, self.objects.values()):
            root.location = campaign
        self._current_object = campaign
        self.current_object_pane = None
        self.locations_pane = None
        self.story_pane = None
        self.status_pane = None
        if self.screen:
            self.init_screen()
            self.main()
        else:
            self.current_object = self.current_object._child_locatables[0]
            print(self.current_object)
            print("  self.locations")
            [print(f"    {o}") for o in self.locations]
            print("  self.current_object._child_locatables")
            [print(f"    {o}") for o in self.current_object._child_locatables]
            print("All Objects:")
            for o in self.objects.values():
                print(o)
                if o.description is not None:
                    print(f"    {recursive_format(o.description, o)}")

    def init_screen(self):
        self.screen.clear()
        self.screen.refresh()

        # Column 1
        x = 0

        self.current_object_pane = TextPane(
            lambda: format(self.current_object, "1"),
            (x,  0),  # Screen Position
            (3, 50),  # Pad Size
            (3, 50),  # Pad Viewport Size
            border_args=[  # Arguments to pad.border()
                curses.ACS_VLINE,  # left side
                curses.ACS_VLINE,  # right side
                curses.ACS_HLINE,  # top side
                curses.ACS_HLINE,  # bottom side
                curses.ACS_ULCORNER,  # top left
                curses.ACS_URCORNER,  # top right
                curses.ACS_LTEE,  # bottom left
                curses.ACS_RTEE,  # bottom right
            ],
        )
        x += self.current_object_pane.height

        self.locations_pane = MenuPane(
            self.locations,
            (x-1, 0),                   # Screen Position
            (len(self.objects), 50),  # Pad Size
            (10, 50),                  # Pad Viewport Size
            border_args=[  # Arguments to pad.border()
                curses.ACS_VLINE,  # left side
                curses.ACS_VLINE,  # right side
                curses.ACS_HLINE,  # top side
                curses.ACS_HLINE,  # bottom side
                curses.ACS_LTEE,  # top left
                curses.ACS_RTEE,  # top right
                curses.ACS_LTEE,  # bottom left
                curses.ACS_RTEE,  # bottom right
            ],
            renderer=lambda i, d: format(d, "0"),
        )
        x += self.locations_pane.height-1

        self.status_pane = TextPane(
            "World Builder",
            (x-1,  0),  # Screen Position
            (3, 50),  # Pad Size
            (3, 50),  # Pad Viewport Size
            border_args=[  # Arguments to pad.border()
                curses.ACS_VLINE,  # left side
                curses.ACS_VLINE,  # right side
                curses.ACS_HLINE,  # top side
                curses.ACS_HLINE,  # bottom side
                curses.ACS_LTEE,  # top left
                curses.ACS_RTEE,  # top right
                curses.ACS_LLCORNER,  # bottom left
                curses.ACS_LRCORNER,  # bottom right
            ],
        )
        x += self.status_pane.height-1

        # Column 2
        height = x
        x = 0
        self.description_pane = TextPane(
            lambda: textwrap.wrap(recursive_format(self.current_object.description, self.current_object), 46),
            (x, 50),  # Screen Position
            (height, 50),  # Pad Size
            (height, 50),  # Pad Viewport Size
        )
        x += self.description_pane.height

        # Row 2
        x = height
        self.story_pane = TextPane(
            lambda: self.story_formatter(),
            (height, 0),  # Screen Position
            (4000, 100),  # Pad Size
            (40, 100),  # Pad Viewport Size
        )

        self.current_object_pane()
        self.description_pane()
        self.status_pane()
        self.description_pane()
        self.story_pane()
        self.locations_pane.set_data(self.locations)

        self.current_object_pane.status_pane = self.status_pane
        self.locations_pane.status_pane = self.status_pane
        self.description_pane.status_pane = self.status_pane

    def _story_formatter(self):
        for passage in self.passages:
            for line in format(passage).splitlines():
                yield ""
                wrapped_lines = textwrap.wrap(line, width=96)
                for wrapped_line in wrapped_lines:
                    yield wrapped_line

    def story_formatter(self):
        story_formatter = self._story_formatter()
        try:
            next(story_formatter)
        except StopIteration:
            return
        for line in story_formatter:
            yield line

    @property
    def current_object(self):
        return self._current_object

    @current_object.setter
    def current_object(self, current_object):
        self._current_object = current_object
        if self.screen:
            self.current_object_pane()
            self.description_pane()
            self.story_pane()
            self.locations_pane.set_data(self.locations)

    @property
    def locations(self):
        return list(filter(lambda o: isinstance(o, Location), self.current_object._child_locatables))

    @property
    def passages(self):
        return list(filter(lambda o: isinstance(o, Passage), self.current_object._child_locatables))

    def main(self):
        while True:
            key = self.screen.getkey()
            if key in {"q", "Q"}:
                break
            elif key in {curses.KEY_UP, "w", "W"}:
                self.locations_pane.up()
            elif key in {curses.KEY_DOWN, "s", "S"}:
                self.locations_pane.down()
            elif key in {"r", "R"}:
                self.story_pane.up()
            elif key in {"f", "F"}:
                self.story_pane.down()
            elif key in {curses.KEY_LEFT, "a", "A"}:
                if self.current_object.location:
                    self.current_object = self.current_object.location
            elif key in {curses.KEY_RIGHT, "d", "D"}:
                if 0 <= self.locations_pane.selected_index < len(self.locations):
                    self.current_object = self.locations_pane.selected


if __name__ == "__main__":
    curses.wrapper(
        UI,
        sys.argv[1],
    )
    # UI(None, "campaign.json")
