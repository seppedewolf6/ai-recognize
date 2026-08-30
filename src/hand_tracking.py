import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def get_landmark_data(hand_landmarks):
    """
    Zet de 21 hand landmarks om naar een lijst
    van 63 waarden: x, y en z per landmark.
    """

    data = []

    for landmark in hand_landmarks.landmark:
        data.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    return data


def normalize_landmarks(hand_landmarks):
    """
    Normaliseert de hand landmarks ten opzichte van de pols.
    Hierdoor is de data minder afhankelijk van de positie
    van de hand in het camerabeeld.
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

while True:
    success, frame = camera.read()

    if not success:
        print("Kan geen beeld van de webcam lezen.")
        break

    # OpenCV gebruikt BGR, Mediapipe RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:
            # Hand tekenen
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Alle landmarks ophalen
            landmark_data = normalize_landmarks(hand_landmarks)

            print(f"Aantal waarden: {len(landmark_data)}")
            print(landmark_data)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
hands.close()
