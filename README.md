# kutanspeech
```py
from kutanspeech import *

ks = kutanspeech()
ks.noice_optimizer()
print("Optimize tamamlandı. Dinleniyor.")

data = ks.listen()
try:
    print(ks.speech_to_text(data, language="tr"))
except UnknownValueError:
    print("Anlaşılmadı")
```

```py
from kutanspeech import *
import time
ks = kutanspeech()
ks.noice_optimizer()
print("Optimize tamamlandı. Dinleniyor.")

def callback(data):
    try:
        text = ks.speech_to_text(data, language="tr")
        print(text)
    except UnknownValueError:
        pass

stopper = ks.background_listener(callback=callback)
while True: time.sleep(0.1)
stopper()
```
