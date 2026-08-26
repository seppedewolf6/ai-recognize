import cv2
import mediapipe as mp
import pygame
import joblib


# =========================
# INSTELLINGEN
# =========================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CONFIDENCE_THRESHOLD = 0.70


# =========================
# AI MODEL
# =========================

model = joblib.load("models/gesture_model.pkl")

print("Gesture model geladen.")


# =========================
# MEDIAPIPE
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
# LANDMARK NORMALISATIE
# =========================

def normalize_landmarks(hand_landmarks):

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
# PYGAME
# =========================

pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "AI Gesture Controller"
)

clock = pygame.time.Clock()


# =========================
# CHARACTER
# =========================

from character import Character

character = Character(
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2
)


# =========================
# WEBCAM
# =========================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Kan de webcam niet openen.")
    pygame.quit()
    exit()


# =========================
# GAME LOOP
# =========================

running = True

while running:

    # =========================
    # PYGAME EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # =========================
    # WEBCAM
    # =========================

    success, frame = camera.read()

    if not success:
        continue


    # BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # =========================
    # HAND DETECTIE
    # =========================

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


        # =========================
        # LANDMARK DATA
        # =========================

        landmark_data = normalize_landmarks(
            hand_landmarks
        )


        # =========================
        # AI VOORSPELLING
        # =========================

        prediction = model.predict([
            landmark_data
        ])

        gesture = prediction[0]


        probabilities = model.predict_proba([
            landmark_data
        ])

        confidence = max(probabilities[0])


        # =========================
        # CHARACTER BESTUREN
        # =========================

        if confidence >= CONFIDENCE_THRESHOLD:

            if gesture == "LEFT":
                character.move_left()

            elif gesture == "RIGHT":
                character.move_right()

            elif gesture == "UP":
                character.move_up()

            elif gesture == "DOWN":
                character.move_down()

            elif gesture == "ACTION":
                character.action()


    # =========================
    # CHARACTER UPDATE
    # =========================

    character.update(
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )


    # =========================
    # PYGAME SCHERM
    # =========================

    screen.fill((30, 30, 30))

    character.draw(screen)


    # =========================
    # AI STATUS
    # =========================

    font = pygame.font.Font(None, 32)

    gesture_text = font.render(
        f"Gesture: {gesture}",
        True,
        (255, 255, 255)
    )

    confidence_text = font.render(
        f"Confidence: {confidence:.0%}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        gesture_text,
        (20, 20)
    )

    screen.blit(
        confidence_text,
        (20, 55)
    )


    pygame.display.flip()

    clock.tick(60)


# =========================
# STOPPEN
# =========================

camera.release()

cv2.destroyAllWindows()

hands.close()

pygame.quit()