# AI Gesture Game

Een kleine AI-game waarbij je een karakter bestuurt met handgebaren via je webcam.

## 1. Installeren

Installeer de dependencies:

```bash
pip install -r requirements.txt
```

Zorg ervoor dat Python 3.11 geïnstalleerd is.

## 2. Handgebaren verzamelen

Start het programma voor het verzamelen van trainingsdata:

```bash
python src/collect_data.py
```

Verzamel voorbeelden voor de volgende gebaren:

* `LEFT` → naar links bewegen
* `RIGHT` → naar rechts bewegen
* `UP` → naar boven bewegen
* `DOWN` → naar beneden bewegen
* `ACTION` → een blok breken

De verzamelde gegevens worden opgeslagen in:

```text
data/gestures.csv
```

## 3. AI-model trainen

Train vervolgens het Random Forest-model:

```bash
python src/train_model.py
```

Het getrainde model wordt opgeslagen als:

```text
models/gesture_model.pkl
```

## 4. Game starten

Start de game:

```bash
python src/ai_game.py
```

Er worden twee vensters geopend:

* **Camera** → toont je hand en het herkende gebaar
* **Game** → toont het karakter en de blokken

## 5. Spelen

Gebruik je hand om het karakter te besturen:

| Gebaar   | Actie        |
| -------- | ------------ |
| `LEFT`   | Naar links   |
| `RIGHT`  | Naar rechts  |
| `UP`     | Naar boven   |
| `DOWN`   | Naar beneden |
| `ACTION` | Blok breken  |

Om een blok te breken moet je karakter **Het blok aanraken**.

Er zit een korte cooldown op `ACTION`, zodat niet meerdere blokken tegelijk worden gebroken.

Breek alle blokken om het spel uit te spelen.

## Projectstructuur

```text
ai-recognize/
│
├── data/
│   └── gestures.csv
│
├── models/
│   └── gesture_model.pkl
│
├── src/
│   ├── camera.py
│   ├── hand_tracking.py
│   ├── collect_data.py
│   ├── train_model.py
│   ├── predict_gesture.py
│   ├── game.py
│   ├── character.py
│   └── ai_game.py
│
└── requirements.txt
```
