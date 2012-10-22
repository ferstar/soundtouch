import ctypes as _ctypes, os as _os

def _setFuncType(func, res, *args):
    func.restype = res
    func.argtypes = args

if _os.name == 'nt':
    _lib = _ctypes.windll.LoadLibrary('SoundTouch')
elif _os.name == 'posix':
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

def getVersionId():
    '''Get SoundTouch library version Id.'''
    return _lib.soundtouch_getVersionId()

def getVersionString():
    '''Get SoundTouch library version string.'''
    return _lib.soundtouch_getVersionString()

####################################

class SoundTouchInstance(object):
    def __init__(self, numChannels, srate):
        self.handle = _lib.soundtouch_createInstance()
        self.setChannels(numChannels)
        self.setSampleRate(srate)

    def __del__(self):
        if _lib != None:
            _lib.soundtouch_destroyInstance(self.handle)

    def setRate(self, newRate):
        '''Sets new rate control value. Normal rate = 1.0, smaller values
        represent slower rate, larger faster rates.'''
        _lib.soundtouch_setRate(self.handle, newRate)

    def setTempo(self, newTempo):
        '''Sets new tempo control value. Normal tempo = 1.0, smaller values
        represent slower tempo, larger faster tempo.'''
        _lib.soundtouch_setTempo(self.handle, newTempo)

    def setRateChange(self, newRate):
        '''Sets new rate control value as a difference in percents compared
        to the original rate (-50 .. +100 %).'''
        _lib.soundtouch_setRateChange(self.handle, newRate)

    def setTempoChange(self, newTempo):
        '''Sets new tempo control value as a difference in percents compared
        to the original tempo (-50 .. +100 %).'''
        _lib.soundtouch_setTempoChange(self.handle, newTempo)

    def setPitch(self, newPitch):
        '''Sets new pitch control value. Original pitch = 1.0, smaller values
        represent lower pitches, larger values higher pitch.'''
        _lib.soundtouch_setPitch(self.handle, newPitch)

    def setPitchOctaves(self, newPitch):
        '''Sets pitch change in octaves compared to the original pitch
        (-1.00 .. +1.00).'''
        _lib.soundtouch_setPitchOctaves(self.handle, newPitch)

    def setPitchSemiTones(self, newPitch):
        '''Sets pitch change in semi-tones compared to the original pitch
        (-12 .. +12).'''
        _lib.soundtouch_setPitchSemiTones(self.handle, newPitch)

    def setChannels(self, numChannels):
        '''Sets the number of channels, 1 = mono, 2 = stereo.'''
        assert numChannels in (1, 2)
        _lib.soundtouch_setChannels(self.handle, numChannels)
        self.channels = numChannels

    def setSampleRate(self, srate):
        '''Sets sample rate.'''
        _lib.soundtouch_setSampleRate(self.handle, srate)

    def flush(self):
        '''Flushes the last samples from the processing pipeline to the output.
        Clears also the internal processing buffers.
        
        Note: This function is meant for extracting the last samples of a sound
        stream. This function may introduce additional blank samples in the end
        of the sound stream, and thus it's not recommended to call this function
        in the middle of a sound stream.'''
        _lib.soundtouch_flush(self.handle)

    def clear(self):
        '''Clears all the samples in the object's output and internal processing
        buffers.'''
        _lib.soundtouch_clear(self.handle)

    def numUnprocessedSamples(self):
        '''Returns number of samples currently unprocessed.'''
        return _lib.soundtouch_numUnprocessedSamples(self.handle)

    def numSamples(self):
        '''Returns number of samples currently available.'''
        return _lib.soundtouch_numSamples(self.handle)

    def isEmpty(self):
        '''Returns True if there aren't any samples available for outputting.'''
        return _lib.soundtouch_isEmpty(self.handle) != 0

    def setSetting(self, settingId, value):
        '''Changes a setting controlling the processing system behaviour. See the
        'SETTING_...' defines for available setting ID's.

        Returns True if the setting was succesfully changed.'''
        return _lib.soundtouch_setSetting(self.handle, settingId, value) != 0

    def getSetting(self, settingId):
        '''Reads a setting controlling the processing system behaviour. See the
        'SETTING_...' defines for available setting ID's.

        Returns the setting value.'''
        return _lib.soundtouch_getSetting(self.handle, settingId)

    def putSamples(self, samples):
        '''Adds samples (an iterable object of floats, in case of stereo-sound,
        two floats for a complete sample) into the input of the object.'''
        size = len(samples)
        data = (_ctypes.c_float * size)(*samples)
        _lib.soundtouch_putSamples(self.handle, data, size / self.channels)

    def receiveSamples(self, maxSamples):
        '''Receive at max 'maxSamples' samples (an iterable object of floats,
        in case of stereo-sound, two floats for a complete sample) from the
        output of the object.'''
        data = (_ctypes.c_float * (maxSamples * self.channels))()
        size = _lib.soundtouch_receiveSamples(self.handle, data, maxSamples)
        return data[: size * self.channels]


def createInstance(numChannels = 2, srate = 44100):
    '''Create a new instance of SoundTouch processor.'''
    return SoundTouchInstance(numChannels, srate)

####################################

SETTING_USE_AA_FILTER = 0
SETTING_AA_FILTER_LENGTH = 1
SETTING_USE_QUICKSEEK = 2
SETTING_SEQUENCE_MS = 3
SETTING_SEEKWINDOW_MS = 4
SETTING_OVERLAP_MS = 5

