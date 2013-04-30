import logging
import random
from threading import Thread, Event
from sounds import Sound

logger = logging.getLogger('scene')
logging.basicConfig(level=logging.ERROR)


class SceneSound(object):
    def __init__(self, path):
        self.path = path
        self.loop = False
        self.start_at = 0
        self.volume = 100
        self.random = 0
        self.fadein = 0
        self.workers = []
        self.stop_event = Event()
        self._sound = None
        self.bind_to = None
        self.auto_start = True

    def play(self, ignore_start_at=False):
        if self.start_at == 0 or ignore_start_at:
            logger.debug('[{0}] Calling start'.format(self.path))
            self._play_sound()
        else:
            logger.debug('Start at is {0} for {1},'
                         ' delaying'.format(self.start_at, self.path))
            p = Thread(target=self._play_sound_delayed)
            self.workers.append(p)
            p.start()

    def stop(self):
        logger.debug('[%s] Received stop', self.path)
        self.stop_event.set()

        for process in self.workers:
            if process.is_alive():
                process.join()
                logger.debug('Joined with %s', process)
            else:
                logger.debug('NOT joined %s because its dead', process)

        if self._sound is not None:
            logger.debug('[%s] stopping sound', self.path)
            self._sound.stop()
            self._sound.destroy()
        else:
            logger.debug('[%s] sound is none', self.path)
            logger.debug('[%s] class is %s', self.path, self)
            logger.debug('[%s] workers are %s', self.path, self.workers)

        self.workers = []
        self.stop_event = Event()
        self._sound = None

    def _play_sound(self):
        if self.stop_event.is_set():
            logger.debug('[%s] Not playing because stop is true', self.path)
            return

        logger.debug('[%s] Playing because stop is false', self.path)
        logger.debug('[%s] and im object %s', self.path, self)

        if self.random == 0:
            if self.fadein > 0:
                logger.debug('[{0}] Running fadein process'.format(self.path))
                self._sound = Sound(self.get_path(), 0)
                self._sound.play(loop=self.loop)
                p = Thread(target=self._fadein)
                self.workers.append(p)
                p.start()
            else:
                logger.debug('Playing {0}'.format(self.path))
                self._sound = Sound(self.get_path(), self.volume)
                self._sound.play(loop=self.loop)
        else:
            p = Thread(target=self._random)
            self.workers.append(p)
            p.start()

    def get_path(self):
        if isinstance(self.path, list):
            return random.choice(self.path)

        return self.path

    def _play_sound_delayed(self):
        logger.debug('[{0}] Sleeping for {1} seconds'.format(self.path,
            self.start_at))
        self.stop_event.wait(self.start_at)
        logger.debug('[{0}] Waking up'.format(self.path))
        if not self.stop_event.is_set():
            self._play_sound()

    def _random(self):
        self._sound = Sound(self.get_path(), self.volume)
        # TODO don't use player
        sound_length = self._sound.player.length

        while not self.stop_event.is_set():
            r = random.random()
            if r <= self.random:
                self._sound = Sound(self.get_path(), self.volume)
                self._sound.play(loop=False)

            self.stop_event.wait(sound_length + 1)

        logger.debug('[%s] Stopping rand', self.path)

    def _fadein(self):
        current_volume = self._sound.get_volume() or 0
        step = 2
        fade_duration = self.fadein

        while current_volume < self.volume and not self.stop_event.is_set():
            self._sound.set_volume(current_volume + step)
            current_volume += step
            self.stop_event.wait(float(fade_duration) / float(self.volume))


class Scene(object):
    def __init__(self, name):
        self.name = name
        self.sounds = []
        self.master_volume = 100

    def play(self):
        for sound in self.sounds:
            sound.volume = sound.volume * (float(self.master_volume) / 100)

            if sound.auto_start:
                sound.play()

    def stop(self):
        for sound in self.sounds:
            logger.debug('[SCENE] Stopping %s', sound.path)
            sound.stop()


class Scenario(object):
    def __init__(self, name):
        self.name = name
        self.scenes = []
