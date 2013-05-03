from scene import Scene, SceneSound, Scenario
from yaml import load


def dict_to_scene(name, scene_dict):
    scene = Scene(name)

    for sound in scene_dict:
        scene_sound = SceneSound(sound['path'])
        scene_sound.volume = sound.get('volume', 100)
        scene_sound.start_at = sound.get('start_at', 0)
        scene_sound.loop = sound.get('loop', False)
        scene_sound.random = sound.get('random', 0)
        scene_sound.fadein = sound.get('fadein', 0)
        scene_sound.bind_to = str(sound.get('bind_to', '')) or None
        scene_sound.auto_start = sound.get('auto_start', True)
        scene.sounds.append(scene_sound)

    return scene


def import_config(contents):
    config = load(contents)
    scenarios = []

    for key in sorted(config.iterkeys(), key=str.lower):
        scenario = Scenario(key)
        scenes = []

        for scene_key in sorted(config[key].iterkeys(), key=str.lower):
            scenes.append(dict_to_scene(scene_key, config[key][scene_key]))

        scenario.scenes = scenes
        scenarios.append(scenario)

    return scenarios
