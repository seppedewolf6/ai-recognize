import cv2
import mediapipe as mp
import joblib


# =========================
# 1. MODEL LADEN
# =========================

model = joblib.load("models/gesture_model.pkl")

print("Gesture model geladen.")


# =========================
# 2. MEDIAPIPE INSTELLEN
# =========================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# =========================
# 3. LANDMARKS NORMALISEREN
# =========================

def normalize_landmarks(hand_landmarks):
    """
    Normaliseert de 21 hand landmarks
    ten opzichte van de pols.
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


# =========================
# 4. WEBCAM OPENEN
# =========================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kan de webcam niet openen.")
    exit()


# =========================
# 5. REALTIME HERKENNING
# =========================

while True:

    success, frame = camera.read()

    if not success:
        print("Kan geen beeld van de webcam lezen.")
        break

    # OpenCV BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # MediaPipe handdetectie
    result = hands.process(rgb_frame)

    gesture = "Geen hand"
    confidence = 0.0

    if result.multi_hand_landmarks:

        hand_landmarks = result.multi_hand_landmarks[0]

        # Hand tekenen
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Zelfde normalisatie als bij training
        landmark_data = normalize_landmarks(
            hand_landmarks
        )

        # Model verwacht een lijst met 63 waarden
        prediction = model.predict([
            landmark_data
        ])

        gesture = prediction[0]

        # Confidence ophalen
        probabilities = model.predict_proba([
            landmark_data
        ])

        confidence = max(probabilities[0])


    # =========================
    # 6. RESULTAAT OP SCHERM
    # =========================

    cv2.putText(
        frame,
        f"GESTURE: {gesture}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"CONFIDENCE: {confidence:.0%}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "AI Gesture Recognition",
        frame
    )


    # =========================
    # 7. STOPPEN
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# 8. OPRUIMEN
# =========================

camera.release()
cv2.destroyAllWindows()
hands.close()