import curses

from world.utilities.partial_proxy import PartialProxy


class Pane(PartialProxy):
    def __init__(self, screen_position, pad_size, pad_viewport_size=None, pad_viewport_top_left=(0, 0), border_args=(), status_pane=None):
        super().__init__(curses.newpad(*pad_size))
        with self.pause_proxy():
            self.screen_position = (screen_position[0]+1, screen_position[1]+1)
            self._border_win = curses.newwin(*pad_viewport_size, *screen_position)
            self.pad_size = (pad_size[0]-2, pad_size[1]-2)
            self.pad_viewport_size = pad_viewport_size if pad_viewport_size is not None else self.pad_size
            self.pad_viewport_top_left = pad_viewport_top_left
            self.border_args = border_args
            self.status_pane = status_pane

    @property
    def height(self):
        return self.pad_viewport_size[0]

    def border(self):
        self._border_win.border(*self.border_args)
        self._border_win.refresh()

    @property
    def bottom_right(self):
        return (
            self.screen_position[0] + self.pad_viewport_size[0] - 3,
            self.screen_position[1] + self.pad_viewport_size[1] - 3,
        )

    def refresh(self):
        self.border()
        self.proxied_object.refresh(
            *self.pad_viewport_top_left,  # Pane coordinate of viewport top left
            *self.screen_position,        # Screen coordinate to place Pane top left
            *self.bottom_right,           # Screen coordinate to place Pane bottom right
        )
