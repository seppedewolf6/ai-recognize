import cv2
import mediapipe as mp
import pygame
import joblib
import pandas as pd

from character import Character


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

# Dezelfde feature-namen als tijdens het trainen
feature_columns = []

for i in range(21):
    feature_columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

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
    "AI Gesture Game"
)

clock = pygame.time.Clock()


# =========================
# CHARACTER
# =========================

character = Character(
    SCREEN_WIDTH // 2,
    400
)


# =========================
# BLOKKEN
# =========================

blocks = [

    pygame.Rect(150, 460, 60, 40),
    pygame.Rect(300, 460, 60, 40),
    pygame.Rect(450, 460, 60, 40),
    pygame.Rect(600, 460, 60, 40)

]


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
    # CAMERA
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

        # Landmarks tekenen
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

        # Maak DataFrame met dezelfde feature-namen
        landmark_data_df = pd.DataFrame(
            [landmark_data],
            columns=feature_columns
        )

        prediction = model.predict(
            landmark_data_df
        )

        gesture = prediction[0]

        probabilities = model.predict_proba(
            landmark_data_df
        )

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
                character.action(blocks)


    # =========================
    # CAMERA INFO
    # =========================

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {confidence:.0%}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # =========================
    # CAMERA VENSTER
    # =========================

    cv2.imshow(
        "Camera - AI Gesture Recognition",
        frame
    )


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


    # =========================
    # GROND
    # =========================

    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (0, 500, SCREEN_WIDTH, 100)
    )


    # =========================
    # BLOKKEN TEKENEN
    # =========================

    for block in blocks:

        pygame.draw.rect(
            screen,
            (120, 80, 40),
            block
        )

        pygame.draw.rect(
            screen,
            (180, 130, 70),
            block,
            3
        )


    # =========================
    # CHARACTER
    # =========================

    character.draw(screen)


    # =========================
    # GAME INFO
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


    # =========================
    # COOLDOWN
    # =========================

    cooldown = character.get_cooldown_remaining()

    if cooldown > 0:

        cooldown_text = font.render(
            f"Action cooldown: {cooldown:.1f}s",
            True,
            (255, 255, 255)
        )

    else:

        cooldown_text = font.render(
            "Action: READY",
            True,
            (255, 255, 255)
        )

    screen.blit(
        cooldown_text,
        (20, 90)
    )


    # =========================
    # UITLEG
    # =========================

    controls_text = font.render(
        "Move with gestures - Action breaks blocks",
        True,
        (255, 255, 255)
    )

    screen.blit(
        controls_text,
        (20, 570)
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