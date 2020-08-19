# kutanspeech
Word by word Speech Recognition Library.

</br>
![alt text](https://i.hizliresim.com/R83tYd.png)
</br>

```py
from kutanspeech import *

ks = kutanspeech()
ks.noice_optimizer()
print("Noice optimized. Listening...")

data = ks.listen()
try:
    print(ks.speech_to_text(data, language="en"))
except UnknownValueError:
    print("I didn't understand what you said")
```

Background listener example;
```py
from kutanspeech import *
import time
ks = kutanspeech()
ks.noice_optimizer()
print("Noice optimized. Listening...")

def callback(data):
    try:
        text = ks.speech_to_text(data, language="en")
        print(text)
    except UnknownValueError:
        pass

stopper = ks.background_listener(callback=callback)
while True: time.sleep(0.1)
stopper()
```
