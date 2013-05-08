import os
from file import load_scenarios


class Application(object):
    CONFIG_FILE_PATH = os.path.expanduser('~/.ampyent')

    def __init__(self):
        self._scenarios = []
        self.current_scene = None

    @property
    def scenarios(self):
        if not self._scenarios:
            try:
                with open(self.CONFIG_FILE_PATH) as file:
                    self._scenarios = load_scenarios(file.read())
            except IOError:
                pass

        return self._scenarios

    def get_scenario_by_name(self, scenario_name):
        for scenario in self.scenarios:
            if scenario.name == scenario_name:
                return scenario

        raise KeyError("Scenario {0} doesn't exist".format(scenario_name))

    def play_scene(self, scene):
        if self.current_scene:
            self.current_scene.stop()

        self.current_scene = scene
        self.current_scene.play()

ampyent_app = Application()
