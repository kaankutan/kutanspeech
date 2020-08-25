# KutanSpeech
Word by word Speech Recognition Library.
</br>

![alt text](https://i.hizliresim.com/R83tYd.png)
</br>

<h3>For install;</h3>
</br>

`pip install KutanSpeech`
</br>

### Word by word listener

This sample actively previews your voice.
</br>

```py
import KutanSpeech as ks

engine = ks.KutanSpeech()
engine.noice_optimizer()
print("Noice optimized. Listening...")

def callback(text):
    print("Preview: "+text)

try:
    text = engine.wordbyword_listen(callback=callback, language="en", timeout_sec = 3)
    print("Sentence: "+text)

except ks.UnknownValueError:
    print("Not understood")

except ks.TimeoutError:
    print("Timeout error")
```
`timeout_sec` is not a mandatory parameter.
</br>

### Listener

This example records and translate to text.

</br>

```py
import KutanSpeech as ks

engine = ks.KutanSpeech()
engine.noice_optimizer()
print("Noice optimized. Listening...")

try:
    data = engine.listen(timeout_sec=3)
    text = engine.speech_to_text(data)
    print(text)

except ks.TimeoutError:
    print("Listening has been timeout")

except ks.UnknownValueError:
    print("Not understood")
    
except ks.RequestError:
    print("Internet connection could not be established")
```
`timeout_sec` is not a mandatory parameter.
</br>

### Background listener example
This example listens to your voice in the background and when it detects a word, it sends the audio data to the callback function.
</br>

```py
import KutanSpeech as ks
import time

engine = ks.KutanSpeech()
engine.noice_optimizer()
print("Noice optimized. Listening...")

def callback(data):
    try:
        text = engine.speech_to_text(data)
        print(text)
    except ks.UnknownValueError:
        pass
        
    except ks.RequestError:
        print("Internet connection could not be established")

stopper = engine.background_listener(callback=callback)
while True: time.sleep(0.1)
stopper()
```
