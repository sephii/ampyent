from mplayer import Player, PIPE


class Sound(object):
    """
    A Sound object is a simple abstraction of an underlying sound that can be
    played, stopped, etc.
    """
    def __init__(self, path, volume=100):
        self.path = path
        # We need to set the volume when creating the mplayer process. If we
        # don't, the sound would start playing at 100% for about 1 sec before
        # the actual volume gets applied
        self.player = Player(stdout=PIPE, stderr=PIPE,
                             args=('-volume {0}'.format(volume)))
        self.player.loadfile(self.path)
        # Pause the stream so we can't do something else before calling play()
        self.player.pause()

    def play(self, loop=False):
        if loop:
            self.player.loop = 0

        self.player.pause()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def get_volume(self):
        return self.player.volume

    def set_volume(self, volume):
        self.player.volume = volume

    def get_duration(self):
        return self.player.length

    def destroy(self):
        self.player.quit()

    def __del__(self):
        self.destroy()
