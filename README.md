# kutanspeech
Word by word Speech Recognition Library.
</br>

![alt text](https://i.hizliresim.com/R83tYd.png)
</br>

Word by word listener example;
```py
import KutanSpeech

ks = KutanSpeech()
ks.noice_optimizer()
print("Noice optimized. Listening...")

def callback(text):
    print("Preview: "text)

try:
    text = ks.wordbyword_listen(callback=callback)
    print("Sentence: "+text)
    
except ks.UnknownValueError:
    print("Not understood")
    
except ks.TimeoutError:
    print("Timeout error")
```
`timeout_sec` is not a mandatory parameter.
</br>

Listener example;
```py
import KutanSpeech

ks = KutanSpeech()
ks.noice_optimizer()
print("Noice optimized. Listening...")

data = ks.listen()

try:
    print(ks.speech_to_text(data))
    
except ks.UnknownValueError:
    print("Not understood")
    
except ks.RequestError:
    print("Internet connection could not be established")
```

Background listener example;
```py
import KutanSpeech
import time

ks = KutanSpeech()
ks.noice_optimizer()
print("Noice optimized. Listening...")

def callback(data):
    try:
        text = ks.speech_to_text(data)
        print(text)
    except ks.UnknownValueError:
        pass
    except ks.RequestError:
        print("Internet connection could not be established")

stopper = ks.background_listener(callback=callback)
while True: time.sleep(0.1)
stopper()
```
