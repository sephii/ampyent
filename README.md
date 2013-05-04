**This project is in very early development stage, don't expect it to work for
you yet.**

Requirements
============

* mplayer
* [mplayer.py](https://github.com/baudm/mplayer.py)
* [PyYAML](https://pypi.python.org/pypi/PyYAML)
* curses-compatible OS (ie. not Windows)

Installation
============

TODO

Usage
=====

Start by creating a configuration file (see [Configuration file syntax][] below).
Then run ampyent by typing `python app.py [part of your scenario name]`. For
example, using the configuration file below, we could type the following to run
the scenario "01 my scenario":

```
python app.py 01
```

This will run ampyent and open your scenario but you'll notice that nothing is
playing. You'll need to press the `p` (for **p**lay) to start your first scene.
Here's a summary of the controls:

* Space: play scene
* `s`: stop
* `right arrow`: next scene
* `q`: quit ampyent

If a scene has some sounds with bindings defined (with the `bind_to` attribute),
you'll see them when switching to that scene. A press on these keys will
make the associated sound to be played.


Configuration file syntax
=========================

Configuration is done with a simple yml file that must be named `~/.ampyent`:

```
"01 my scenario":
    "01 my first scene":
        - path:   /home/me/sounds/great_music.wav
          loop:   true
          fade_in: 5

        - path:
              - /home/me/sounds/wolves1.wav
              - /home/me/sounds/wolves2.wav
          loop:     false
          start_at: 10
          volume:   70
          random:   0.2
          bind_to:  1

    "02 my second scene":
        - path: /home/me/sounds/thunder.wav
          loop: true
```

Here's a list of the options you can set for each sound:

* **path**: the absolute path to the sound file that will be played. Any format
  supported by mplayer should be fine. There's no default since this option is
  mandatory.
* **auto_start**: set to false if you don't want this sound to be played
  automatically. Useful for sounds you only want to trigger manually. Default:
  `true`.
* **bind_to**: the key to bind this sound to. You can enter any letter or
  number here. Special keys (like Fx keys) are not supported yet. There's no
  default value for this option.
* **fade_in**: the duration in seconds during which the sound should fade in.
  Default: `0`.
* **loop**: set to true if you want the sound to be played in loop. Default:
  `false`.
* **random**: this value goes on a scale from 0 to 1. Setting this to 0 will
  disable the random mode. If you set this value to anything else, at every X
  seconds (X being the duration of the sound), the sound will have a `random`
  probability of being played. Default: `0`.
* **start_at**: the time, in seconds, at which the sound should start playing.
  It also works in `random` mode and can be used to make sure a sound doesn't
  start playing before the given time. Default: `0`.
* **volume**: the volume of the sound, on a 0-100 scale. Default: `100`.
