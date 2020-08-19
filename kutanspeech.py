from sys import byteorder
from array import array
import pyaudio
import speech_recognition as sr
from threading import Thread
import wave


class TimeoutError(Exception): pass

class RequestError(Exception): pass

class UnknownValueError(Exception): pass

class kutanspeech():
    def __init__(self, RATE = 44100, FORMAT = pyaudio.paInt16, CHUNK_SIZE = 1024, THRESHOLD = 300):
        self._recognizer = sr.Recognizer()
        self._THRESHOLD = 300
        self._CHUNK_SIZE = CHUNK_SIZE
        self._FORMAT = FORMAT
        self._RATE = RATE

    def __is_silent(self, snd_data):
        return max(snd_data) < self._THRESHOLD

    def __normalize(self, snd_data):
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def __trim(self, snd_data):
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self._THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        snd_data = _trim(snd_data)

        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def __add_silence(self, snd_data, seconds):
        silence = [0] * int(seconds * self._RATE)
        r = array('h', silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    def noice_optimizer(self):
        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source)
        self._THRESHOLD = self._recognizer.energy_threshold

    def background_listener(self, callback, sec_for_pause = 0.1, callback_block = False):
        def stopper(): listening_is_active = False
        listening_is_active = True

        def listen_thread():
            while listening_is_active:
                try:
                    data = self.listen(timeout_sec=1, sec_for_stop = sec_for_pause)

                    if callback_block:
                        callback(data)
                    else:
                        Thread(target = callback, args={data}, daemon = True).start()
                except TimeoutError:
                    pass

                if not listening_is_active:
                    break
            
        Thread(target = listen_thread, daemon = True).start()
        return stopper
        
    def listen(self, timeout_sec = None, sec_for_stop = 0.8):
        p = pyaudio.PyAudio()
        stream = p.open(format=self._FORMAT, channels=1, rate=self._RATE,
            input=True, output=True,
            frames_per_buffer=self._CHUNK_SIZE)
        num_silent = 0
        snd_started = False
        timeout = 0
        r = array('h')

        while True:
            snd_data = array('h', stream.read(self._CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            silent = self.__is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1

            elif not silent and not snd_started:
                snd_started = True

            if timeout_sec:
                if silent and not snd_started:
                    timeout += 1
                else:
                    timeout = 0
                if timeout > 32 * timeout_sec:
                    raise TimeoutError("Listen has been timeout.")
                    
            if snd_started and num_silent > 32 * sec_for_stop:
                break

        sample_width = p.get_sample_size(self._FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.__normalize(r)
        r = self.__trim(r)
        r = self.__add_silence(r, 1)
        return sr.AudioData(sample_width = sample_width, sample_rate = self._RATE, frame_data = r)

    def speech_to_text(self, data, language = "en-US"):
        try:
            return self._recognizer.recognize_google(data, language=language)
        except sr.UnknownValueError:
            raise UnknownValueError()
        except sr.RequestError:
            raise RequestError()