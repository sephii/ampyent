**This project is in very early development stage, don't expect it to work for
you yet.**

Requirements
============

* mplayer
* [mplayer.py](https://github.com/baudm/mplayer.py)
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

* `p`: play scene
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
          fadein: 5

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
