import ctypes as _ctypes, os as _os

def _setFuncType(func, res, *args):
    func.restype = res
    func.argtypes = args

if os.name == 'nt':
    _lib = _ctypes.windll.LoadLibrary('SoundTouch')
elif os.name == 'posix':
    _lib = _ctypes.cdll.LoadLibrary('SoundTouch')

_setFuncType(_lib.soundtouch_getVersionId, _ctypes.c_uint)
_setFuncType(_lib.soundtouch_getVersionString, _ctypes.c_char_p)

_setFuncType(_lib.soundtouch_createInstance, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_destroyInstance, None, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_setRate, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setTempo, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setRateChange, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setTempoChange, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setPitch, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setPitchOctaves, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setPitchSemiTones, None, _ctypes.c_void_p, _ctypes.c_float)
_setFuncType(_lib.soundtouch_setChannels, None, _ctypes.c_void_p, _ctypes.c_uint)
_setFuncType(_lib.soundtouch_setSampleRate, None, _ctypes.c_void_p, _ctypes.c_uint)

_setFuncType(_lib.soundtouch_flush, None, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_clear, None, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_numUnprocessedSamples, _ctypes.c_uint, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_numSamples, _ctypes.c_uint, _ctypes.c_void_p)
_setFuncType(_lib.soundtouch_isEmpty, _ctypes.c_int, _ctypes.c_void_p)

_setFuncType(_lib.soundtouch_setSetting, _ctypes.c_int, _ctypes.c_void_p, _ctypes.c_int, _ctypes.c_int)
_setFuncType(_lib.soundtouch_getSetting, _ctypes.c_int, _ctypes.c_void_p, _ctypes.c_int)

_setFuncType(_lib.soundtouch_putSamples, None, _ctypes.c_void_p, _ctypes.POINTER(_ctypes.c_float), _ctypes.c_uint)
_setFuncType(_lib.soundtouch_receiveSamples, _ctypes.c_uint, _ctypes.c_void_p, _ctypes.POINTER(_ctypes.c_float), _ctypes.c_uint)


####################################

getVersionId = _lib.soundtouch_getVersionId
getVersionString = _lib.soundtouch_getVersionString

####################################

class createInstance(object):
    def __init__(self):
        self.handle = _lib.soundtouch_createInstance()
        self.setChannels(2)
        self.setSampleRate(44100)

    def __del__(self):
        if _lib != None:
            _lib.soundtouch_destroyInstance(self.handle)

    def setRate(self, newRate):
        _lib.soundtouch_setRate(self.handle, newRate)

    def setTempo(self, newTempo):
        _lib.soundtouch_setTempo(self.handle, newTempo)

    def setRateChange(self, newRate):
        assert newRate >= -50. and newRate <= 100.
        _lib.soundtouch_setRateChange(self.handle, newRate)

    def setTempoChange(self, newTempo):
        assert newTempo >= -50. and newTempo <= 100.
        _lib.soundtouch_setTempoChange(self.handle, newTempo)

    def setPitch(self, newPitch):
        _lib.soundtouch_setPitch(self.handle, newPitch)

    def setPitchOctaves(self, newPitch):
        assert newPitch >= -1. and newRate <= 1.
        _lib.soundtouch_setPitchOctaves(self.handle, newPitch)

    def setPitchSemiTones(self, newPitch):
        assert newPitch >= -12. and newRate <= 12.
        _lib.soundtouch_setPitchSemiTones(self.handle, newPitch)

    def setChannels(self, numChannels):
        assert numChannels in (1, 2)
        _lib.soundtouch_setChannels(self.handle, numChannels)
        self.channels = numChannels

    def setSampleRate(self, srate):
        _lib.soundtouch_setSampleRate(self.handle, srate)

    def flush(self):
        _lib.soundtouch_flush(self.handle)

    def clear(self):
        _lib.soundtouch_clear(self.handle)

    def numUnprocessedSamples(self):
        return _lib.soundtouch_numUnprocessedSamples(self.handle)

    def numSamples(self):
        return _lib.soundtouch_numSamples(self.handle)

    def isEmpty(self):
        return _lib.soundtouch_isEmpty(self.handle) != 0

    def setSetting(self, settingId, value):
        return _lib.soundtouch_setSetting(self.handle, settingId, value)

    def getSetting(self, settingId):
        return _lib.soundtouch_getSetting(self.handle, settingId)

    def putSamples(self, samples):
        size = len(samples)
        data = (_ctypes.c_float * size)(*samples)
        _lib.soundtouch_putSamples(self.handle, data, size / self.channels)

    def receiveSamples(self, maxSamples):
        data = (_ctypes.c_float * (maxSamples * self.channels))()
        size = _lib.soundtouch_receiveSamples(self.handle, data, maxSamples)
        return data[: size * self.channels]


####################################

SETTING_USE_AA_FILTER = 0
SETTING_AA_FILTER_LENGTH = 1
SETTING_USE_QUICKSEEK = 2
SETTING_SEQUENCE_MS = 3
SETTING_SEEKWINDOW_MS = 4
SETTING_OVERLAP_MS = 5

