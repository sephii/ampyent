import logging
import random
from threading import Thread, Event

from sounds import Sound

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SceneSound(object):
    def __init__(self, path):
        self.path = path
        self.loop = False
        self.start_at = 0
        self.volume = 100
        self.random = 0
        self.fade_in = 0
        self.workers = []
        self.stop_event = Event()
        self._sound = None
        self.bind_to = None
        self.auto_start = True

    def play(self):
        if self.start_at == 0:
            self._play_no_delay()
        else:
            p = Thread(target=self._play_delayed)
            self.workers.append(p)
            p.start()

    def play_now(self):
        self._play_no_delay(ignore_random=True)

    def stop(self):
        logger.debug("[%s] Received stop", self.path)
        self.stop_event.set()

        for process in self.workers:
            process.join()

        if self._sound is not None:
            self._sound.destroy()

        self.workers = []
        self.stop_event = Event()
        self._sound = None

    def get_single_path(self):
        """
        Returns the path of the file to play. The path can either be a string,
        or a list. In the latter case, one of the paths in the list will be
        picked randomly.
        """
        if isinstance(self.path, list):
            return random.choice(self.path)

        return self.path

    def _play_no_delay(self, ignore_random=False):
        # This is useful in the case where a thread comes out from sleep
        # and tries to play a sound while it has been stopped in the
        # meantime (eg. delayed play)
        if self.stop_event.is_set():
            logger.debug("[%s] Wanted to be played but not doing so"
                         " because it\'s been stopped", self.path)
            return

        if self.random == 0 or ignore_random:
            if self.fade_in > 0:
                logger.debug("[%s] Playing sound with volume=0 and running"
                             " fade in process", self.path)
                target_volume = self.volume
                self.volume = 0
                self._play_sound()

                p = Thread(target=self._fade_in, args=(target_volume,))
                self.workers.append(p)
                p.start()
            else:
                logger.debug("[%s] Playing", self.path)
                self._play_sound()
        else:
            # Random sounds can't be looped because it would make no sense
            self.loop = False

            logger.debug("[%s] Running random play thread", self.path)
            p = Thread(target=self._random)
            self.workers.append(p)
            p.start()

    def _play_sound(self):
        self._sound = Sound(self.get_single_path(), self.volume)
        self._sound.play(loop=self.loop)

    def _play_delayed(self):
        logger.debug("[%s] Delaying for %s seconds", self.path, self.start_at)
        self.stop_event.wait(self.start_at)
        logger.debug("[%s] It's time to play", self.path)
        self._play_no_delay()

    def _random(self):
        # We need to create a first instance of the sound to get its duration
        self._sound = Sound(self.get_single_path(), self.volume)
        sound_duration = self._sound.get_duration()

        while not self.stop_event.is_set():
            r = random.random()

            if r <= self.random:
                self._play_sound()

            self.stop_event.wait(sound_duration + 1)

        logger.debug('[%s] Stopping rand', self.path)

    def _fade_in(self, target_volume):
        step = 2
        step_delay = float(self.fade_in) / float(target_volume)

        while self.volume < target_volume and not self.stop_event.is_set():
            self._sound.set_volume(self.volume + step)
            self.volume += step
            self.stop_event.wait(step_delay)


class Scene(object):
    def __init__(self, name):
        self.name = name
        self.sounds = []
        self.master_volume = 100

    def play(self):
        for sound in self.sounds:
            # Apply master volume to all scene sounds
            sound.volume = sound.volume * (float(self.master_volume) / 100)

            if sound.auto_start:
                sound.play()

    def stop(self):
        for sound in self.sounds:
            logger.debug('[Scene %s] Stopping %s', self.name, sound.path)
            sound.stop()


class Scenario(object):
    def __init__(self, name):
        self.name = name
        self.scenes = []
