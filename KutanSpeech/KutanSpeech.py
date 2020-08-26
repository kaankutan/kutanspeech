from sys import byteorder
from array import array
import pyaudio
import speech_recognition as sr
import threading

class TimeoutError(Exception): pass

class RequestError(Exception): pass

class UnknownValueError(Exception): pass

class KutanSpeech():
    def __init__(self, RATE = 44100, FORMAT = pyaudio.paInt16, CHUNK_SIZE = 1024, THRESHOLD = 300):
        self._recognizer = sr.Recognizer()
        self.THRESHOLD = 300
        self._CHUNK_SIZE = CHUNK_SIZE
        self._FORMAT = FORMAT
        self._RATE = RATE

    def __is_silent(self, snd_data):
        return max(snd_data) < self.THRESHOLD

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
                if not snd_started and abs(i)>self.THRESHOLD:
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

    def noice_optimizer(self, duration = 1):
        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=duration)
        self.THRESHOLD = self._recognizer.energy_threshold * duration + 50

    def background_listener(self, callback, sec_for_pause = 0.15, callback_block = False):
        def stopper(): listening_is_active = False
        listening_is_active = True

        def listen_thread():
            while listening_is_active:
                try:
                    data = self.listen(timeout_sec=1, sec_for_stop = sec_for_pause)

                    if callback_block:
                        callback(data)
                    else:
                        threading.Thread(target = callback, args={data}, daemon = True).start()
                except TimeoutError:
                    pass

                if not listening_is_active:
                    break
                    SystemExit

        threading.Thread(target = listen_thread, daemon = True).start()
        return stopper

    def wordbyword_listen(self, callback, timeout_sec = None, sec_for_stop = 2, language = "en-US"):
        p = pyaudio.PyAudio()
        self._thread_is_active = False
        self._listen_is_finished = False
        stream = p.open(format=self._FORMAT, channels=1, rate=self._RATE,
            input=True, output=True,
            frames_per_buffer=self._CHUNK_SIZE)
        num_silent = 0
        snd_started = False
        timeout = 0
        r = array('h')

        def previewCallBack(data, callback):
            try:
                text = self.speech_to_text(data, language=language)
                if not self._listen_is_finished:
                    callback(text)
                self._thread_is_active = False
            except Exception:
                self._thread_is_active = False

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

            elif not silent and snd_started:
                num_silent = 0

            if timeout_sec:
                if silent and not snd_started:
                    timeout += 1
                else:
                    timeout = 0
                if timeout > 32 * timeout_sec:
                    raise TimeoutError("Listen has been timeout.")

            if snd_started and num_silent > 32 * sec_for_stop:
                sample_width = p.get_sample_size(self._FORMAT)
                data = sr.AudioData(sample_width = sample_width, sample_rate = self._RATE, frame_data = r)
                return self.speech_to_text(data, language=language)
                self._listen_is_finished = True
                break

            elif snd_started and num_silent > 2 and not self._thread_is_active:
                self._thread_is_active = True
                sample_width = p.get_sample_size(self._FORMAT)
                data = sr.AudioData(sample_width = sample_width, sample_rate = self._RATE, frame_data = r)
                self.thread = threading.Thread(target=previewCallBack, args={data, callback}, daemon = True)
                self.thread.start()


    def listen(self, timeout_sec = None, sec_for_stop = 1):
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

            elif not silent and snd_started:
                num_silent = 0

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
