import curses
import os
import sys
from file import load_scenarios

with open(os.path.expanduser('~/.ampyent'), 'r') as file:
    scenarios = load_scenarios(file.read())

scenario_name = sys.argv[1]

chosen_scenario = None
for scenario in scenarios:
    if scenario.name.startswith(scenario_name):
        chosen_scenario = scenario
        break

if chosen_scenario is None:
    raise Exception('Could not find scenario {0}'.format(scenario_name))


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.addstr('Using scenario ', curses.color_pair(1))
    stdscr.addstr('{0}.\n'.format(chosen_scenario.name.encode('utf-8')), curses.A_BOLD | curses.color_pair(1))
    stdscr.refresh()

    current_scene_id = 0
    scenes = chosen_scenario.scenes

    while 1:
        c = stdscr.getch()

        if c == ord(' '):
            stdscr.addstr('Playing scene ')
            stdscr.addstr(scenes[current_scene_id].name.encode('utf-8'), curses.A_BOLD)
            try:
                next_scene = scenes[current_scene_id + 1]
                stdscr.addstr(' (next scene is {0})'.format(next_scene.name.encode('utf-8')))
            except IndexError:
                stdscr.addstr(' (last scene)')
            stdscr.addstr('\n')
            bindings = {}
            for sound in scenes[current_scene_id].sounds:
                if sound.bind_to is not None:
                    bindings[sound.bind_to] = sound.path

            if bindings:
                stdscr.addstr('You can use the following sounds:\n')
                for binding, sound in bindings.iteritems():
                    stdscr.addstr('{0}: {1}\n'.format(binding, sound))

            scenes[current_scene_id].play()
        elif c == ord('q'):
            scenes[current_scene_id].stop()
            break
        elif c == ord('s'):
            scenes[current_scene_id].stop()
        elif c == curses.KEY_RIGHT:
            scenes[current_scene_id].stop()
            current_scene_id += 1
            stdscr.addstr('Playing scene ')
            stdscr.addstr(scenes[current_scene_id].name, curses.A_BOLD)
            try:
                next_scene = scenes[current_scene_id + 1]
                stdscr.addstr(' (next scene is {0})'.format(next_scene.name.encode('utf-8')))
            except IndexError:
                stdscr.addstr(' (last scene)')
            stdscr.addstr('\n')
            bindings = {}
            for sound in scenes[current_scene_id].sounds:
                if sound.bind_to is not None:
                    bindings[sound.bind_to] = sound.path

            if bindings:
                stdscr.addstr('You can use the following sounds:\n')
                for binding, sound in bindings.iteritems():
                    stdscr.addstr('{0}: {1}\n'.format(binding, sound))

            scenes[current_scene_id].play()
        else:
            for sound in scenes[current_scene_id].sounds:
                if sound.bind_to is not None and c == ord(sound.bind_to):
                    stdscr.addstr('playing {0}\n'.format(sound.path))
                    sound.play_now()

curses.wrapper(main)
