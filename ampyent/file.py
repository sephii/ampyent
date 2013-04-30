import json
from collections import OrderedDict
from scene import Scene, SceneSound, Scenario


def export_scene(scene):
    export = []

    for sound in scene.sounds:
        export.append({
            'path': sound.path,
            'volume': sound.volume,
            'start_at': sound.start_at,
            'loop': sound.loop,
        })

    return json.dumps(export)


def import_scene(scene_contents):
    scene = Scene()
    imported_data = json.loads(scene_contents)

    for sound in imported_data:
        scene_sound = SceneSound(sound['path'])
        scene_sound.volume = sound['volume']
        scene_sound.start_at = sound['start_at']
        scene_sound.loop = sound['loop']

        scene.sounds.append(scene_sound)

    return scene


def dict_to_scene(name, scene_dict):
    scene = Scene(name)

    for sound in scene_dict:
        scene_sound = SceneSound(sound['path'])
        scene_sound.volume = sound.get('volume', 100)
        scene_sound.start_at = sound.get('start_at', 0)
        scene_sound.loop = sound.get('loop', False)
        scene_sound.random = sound.get('random', 0)
        scene_sound.fadein = sound.get('fadein', 0)
        scene_sound.bind_to = sound.get('bind_to', None)
        scene_sound.auto_start = sound.get('auto_start', True)
        scene.sounds.append(scene_sound)

    return scene


def import_config(contents):
    config = json.loads(contents)
    scenarios = []

    for key in sorted(config.iterkeys(), key=unicode.lower):
        scenario = Scenario(key)
        scenes = []

        for scene_key in sorted(config[key].iterkeys(), key=unicode.lower):
            scenes.append(dict_to_scene(scene_key, config[key][scene_key]))

        scenario.scenes = scenes
        scenarios.append(scenario)

    return scenarios
