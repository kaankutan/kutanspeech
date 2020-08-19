# kutanspeech
Word by word speech recognition.

```py
from kutanspeech import *

ks = kutanspeech()
ks.noice_optimizer()
print("Optimize is complicated. Listening.")

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
print("Optimize is complicated. Listening..")

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
