import logging
import os
import sys

from file import load_scenarios
from ui.curses_ui import MainWindow


class AmpyentController(object):
    CONFIG_FILE_PATH = os.path.expanduser('~/.ampyent')

    def __init__(self):
        logging.basicConfig(level=logging.ERROR)
        self.scenario = None
        self.current_scene_id = 0

        if len(sys.argv) < 2:
            raise Exception("Usage: ampyent scenario_name")

        if not os.path.exists(self.CONFIG_FILE_PATH):
            raise Exception("Error: config file {0} doesn't exist",
                            self.CONFIG_FILE_PATH)

        with open(self.CONFIG_FILE_PATH) as file:
            scenarios = load_scenarios(file.read())

        scenario_name = sys.argv[1]
        self.ui = MainWindow()

        for scenario in scenarios:
            if scenario.name.startswith(scenario_name):
                self.scenario = scenario
                break

        if self.scenario is None:
            raise Exception(
                'Could not find scenario {0}'.format(scenario_name)
            )

        self.ui.bind_action(MainWindow.ACTION_PLAY, self.play_current_scene)
        self.ui.bind_action(MainWindow.ACTION_STOP, self.stop_current_scene)
        self.ui.bind_action(MainWindow.ACTION_NEXT, self.next_scene)
        self.ui.bind_action(MainWindow.ACTION_BINDING, self.handle_binding)
        self.ui.bind_action(MainWindow.ACTION_QUIT, self.quit)

        self.ui.start_screen(self.scenario)
        self.ui.input_loop()

    def get_current_scene(self):
        return self.scenario.scenes[self.current_scene_id]

    def get_next_scene(self):
        try:
            next_scene = self.scenario.scenes[self.current_scene_id + 1]
        except IndexError:
            next_scene = None

        return next_scene

    def play_current_scene(self):
        self.ui.show_playing_scene(self.get_current_scene(),
                                   self.get_next_scene())
        self.get_current_scene().play()

    def stop_current_scene(self):
        self.get_current_scene().stop()

    def next_scene(self):
        self.stop_current_scene()
        self.current_scene_id += 1

        try:
            self.play_current_scene()
        except IndexError:
            self.current_scene_id -= 1

    def handle_binding(self, sound):
        sound.play_now()

    def quit(self):
        self.stop_current_scene()


def main():
    AmpyentController()

if __name__ == '__main__':
    main()
