from scene import Scene, SceneSound, Scenario
from yaml import load, Loader


def construct_yaml_str(self, node):
    # Override the default string handling function
    # to always return unicode objects
    # http://stackoverflow.com/questions/2890146/how-to-force-pyyaml-to-load-strings-as-unicode-objects/2967461
    return self.construct_scalar(node)
Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def dict_to_scene(name, scene_dict):
    """
    Transforms a dict to a scene. The name of the keys in the dictionary should
    be the names used in the SceneSound object (volume, start_at, etc).
    """
    scene = Scene(name)
    # List of attributes we should care about
    attrs = ['volume', 'start_at', 'loop', 'random', 'fade_in', 'bind_to',
             'auto_start']

    for sound in scene_dict:
        scene_sound = SceneSound(sound['path'])

        for attr in attrs:
            if attr in sound:
                setattr(scene_sound, attr, sound[attr])

        # bind_to should always be a string, not a numeric
        if scene_sound.bind_to is not None:
            scene_sound.bind_to = str(scene_sound.bind_to)

        scene.sounds.append(scene_sound)

    return scene


def load_scenarios(stream):
    config = load(stream)
    scenarios = []

    # Sort scenarios by name, ascending, and create corresponding Scenario
    # objects
    for key in sorted(config.iterkeys(), key=unicode.lower):
        scenario = Scenario(key)

        # Sort scenes by name, ascending, create corresponding Scene object and
        # attach it to the scenario
        for scene_key in sorted(config[key].iterkeys(), key=unicode.lower):
            scenario.scenes.append(
                dict_to_scene(scene_key, config[key][scene_key])
            )

        scenarios.append(scenario)

    return scenarios
