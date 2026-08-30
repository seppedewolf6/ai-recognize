import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def normalize_landmarks(hand_landmarks):
    """
    Normaliseert de hand landmarks ten opzichte van de pols.
    """

    landmarks = hand_landmarks.landmark

    wrist_x = landmarks[0].x
    wrist_y = landmarks[0].y
    wrist_z = landmarks[0].z

    data = []

    for landmark in landmarks:
        data.extend([
            landmark.x - wrist_x,
            landmark.y - wrist_y,
            landmark.z - wrist_z
        ])

    return data


# Maak de data-map als die nog niet bestaat
os.makedirs("../data", exist_ok=True)

file_path = "../data/gestures.csv"

# Maak CSV-bestand aan
file_exists = os.path.exists(file_path)

file = open(file_path, mode="a", newline="")

writer = csv.writer(file)

# CSV-header
if not file_exists:
    header = []

    for i in range(21):
        header.extend([
            f"x{i}",
            f"y{i}",
            f"z{i}"
        ])

    header.append("label")

    writer.writerow(header)

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kan de webcam niet openen.")
    exit()

print()
print("================================")
print("      AI GESTURE DATASET")
print("================================")
print()
print("U = UP")
print("D = DOWN")
print("L = LEFT")
print("R = RIGHT")
print("A = ACTION")
print("Q = STOP")
print()
print("Maak een gebaar en druk de")
print("bijbehorende toets in.")
print()

current_label = None
samples_collected = 0

while True:

    success, frame = camera.read()

    if not success:
        print("Kan geen beeld van de webcam lezen.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:

        hand_landmarks = result.multi_hand_landmarks[0]

        # Teken landmarks
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Normaliseer landmarks
        landmark_data = normalize_landmarks(hand_landmarks)

        # Als er een label geselecteerd is, slaan we de data op.
        if current_label is not None:
            writer.writerow(
                landmark_data + [current_label]
            )

            file.flush()

            samples_collected += 1

    # Toon huidige status op het scherm
    cv2.putText(
        frame,
        f"Label: {current_label}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Samples: {samples_collected}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Gesture Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("u"):
        current_label = "UP"
        print("Collecting: UP")

    elif key == ord("d"):
        current_label = "DOWN"
        print("Collecting: DOWN")

    elif key == ord("l"):
        current_label = "LEFT"
        print("Collecting: LEFT")

    elif key == ord("r"):
        current_label = "RIGHT"
        print("Collecting: RIGHT")

    elif key == ord("a"):
        current_label = "ACTION"
        print("Collecting: ACTION")

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
hands.close()
file.close()

print()
print(f"Dataset opgeslagen in: {file_path}")
print(f"Totaal aantal samples: {samples_collected}")
