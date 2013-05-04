import curses
import locale


class MainWindow(object):
    ACTION_PLAY = 1
    ACTION_STOP = 2
    ACTION_NEXT = 3
    ACTION_QUIT = 4
    ACTION_BINDING = 5

    KEY_BINDINGS = {
        ord(' '): ACTION_PLAY,
        ord('s'): ACTION_STOP,
        curses.KEY_RIGHT: ACTION_NEXT,
        ord('q'): ACTION_QUIT,
    }

    def __init__(self):
        self.bindings = {}
        self.custom_bindings = {}

        locale.setlocale(locale.LC_ALL, '')
        self.encoding = locale.getpreferredencoding()

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.stdscr.keypad(1)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def quit(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def curses_wrapper(self, stdscr):
        self.stdscr = stdscr

    def bind_action(self, action, callback):
        self.bindings[action] = callback

    def start_screen(self, scenario):
        self.stdscr.addstr('Using scenario ', curses.color_pair(1))
        self.stdscr.addstr('{0}.\n'.format(self._encode(scenario.name)),
                           curses.A_BOLD | curses.color_pair(1))
        self.stdscr.refresh()

    def show_playing_scene(self, current_scene, next_scene=None):
        self.custom_bindings = {}
        scene_bindings = current_scene.get_bindings()
        for key, sound in scene_bindings.iteritems():
            self.custom_bindings[ord(key)] = sound
        self.stdscr.addstr('Playing scene ')
        self.stdscr.addstr(self._encode(current_scene.name), curses.A_BOLD)

        if next_scene:
            self.stdscr.addstr(' (next scene is {0})'.format(
                self._encode(next_scene.name))
            )

        if scene_bindings:
            self.stdscr.addstr('You can use the following sounds:\n')
            for key, sound in scene_bindings.iteritems():
                self.stdscr.addstr('{0}: {1}\n'.format(
                    self._encode(key), self._encode(sound.path))
                )

        self.stdscr.addstr('\n')

    def input_loop(self):
        while 1:
            c = self.stdscr.getch()

            if c in self.KEY_BINDINGS:
                if self.KEY_BINDINGS[c] in self.bindings:
                    self.bindings[self.KEY_BINDINGS[c]]()

                if self.KEY_BINDINGS[c] == self.ACTION_QUIT:
                    self.quit()
                    break
            elif c in self.custom_bindings:
                self.bindings[self.ACTION_BINDING](self.custom_bindings[c])

    def _encode(self, string):
        return string.encode(self.encoding)
