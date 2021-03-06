from pygame import time


class Time:
    _clock = time.Clock()
    _fps = 60
    _playTime = 0.0
    _timeScale = 1.0

    @staticmethod
    def tick_Internal():
        milliseconds = Time._clock.tick(Time._fps)
        Time._playTime += milliseconds / 1000.0

    @staticmethod
    def getDeltaTime():
        milliseconds = Time._clock.get_time()
        return milliseconds / 1000.0

    @staticmethod
    def getPlayTime():
        return Time._playTime

    @staticmethod
    def getFps():
        return Time._clock.get_fps()

    @staticmethod
    def setFps(fps):
        Time._fps = fps

    @staticmethod
    def getTimeScale():
        return Time._timeScale

    @staticmethod
    def setTimeScale(timeScale):
        if (timeScale < 0.0):
            timeScale = 0.0

        Time._timeScale = timeScale
