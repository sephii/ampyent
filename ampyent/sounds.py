from mplayer import Player, PIPE


class Sound(object):
    def __init__(self, path, volume=100):
        self.path = path
        self.player = Player(stdout=PIPE, stderr=PIPE, args=('-volume {0}'.format(volume)))
        self.player.loadfile(self.path)
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

    def destroy(self):
        self.player.quit()

    def __del__(self):
        self.destroy()
