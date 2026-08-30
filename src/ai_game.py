import cv2
import mediapipe as mp
import pygame
import joblib
import pandas as pd

from character import Character

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CONFIDENCE_THRESHOLD = 0.70

# Laad model uit models map
model = joblib.load("models/gesture_model.pkl")

feature_columns = []

for i in range(21):
    feature_columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

print("Gesture model geladen.")

# markers op hand
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# normaliseren van de hand landmarks ten opzichte van de pols
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


# Blokken voor het speelveld maken
def create_blocks():
    return [

        pygame.Rect(100, 460, 60, 40),
        pygame.Rect(220, 460, 60, 40),
        pygame.Rect(340, 460, 60, 40),
        pygame.Rect(460, 460, 60, 40),
        pygame.Rect(580, 460, 60, 40),
        pygame.Rect(700, 460, 60, 40)

    ]


# Pygame starten
pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "AI Gesture Game"
)

clock = pygame.time.Clock()

# Character init
character = Character(
    SCREEN_WIDTH // 2,
    400
)

GAME_PLAYING = "playing"
GAME_FINISHED = "finished"

game_state = GAME_PLAYING

blocks = create_blocks()

previous_gesture = ""

# Webcam openen

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kan de webcam niet openen.")

    pygame.quit()
    exit()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    success, frame = camera.read()

    if not success:
        continue

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    result = hands.process(rgb_frame)

    gesture = "Geen hand"
    confidence = 0.0

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        landmark_data = normalize_landmarks(
            hand_landmarks
        )

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

    action_pressed = (
            gesture == "ACTION"
            and confidence >= CONFIDENCE_THRESHOLD
            and previous_gesture != "ACTION"
    )

    if game_state == GAME_PLAYING:

        if confidence >= CONFIDENCE_THRESHOLD:

            if gesture == "LEFT":

                character.move_left()

            elif gesture == "RIGHT":

                character.move_right()

            elif gesture == "UP":

                character.move_up()

            elif gesture == "DOWN":

                character.move_down()

            elif action_pressed:

                character.action(blocks)

        # Einde spel
        if len(blocks) == 0:
            game_state = GAME_FINISHED

            print("Alle blokken zijn gebroken!")
            print("GEFELICITEERD, JE HEBT GEWONNEN!")

    character.update(
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    screen.fill(
        (30, 30, 30)
    )

    if game_state == GAME_PLAYING:

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (
                0,
                500,
                SCREEN_WIDTH,
                100
            )
        )

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

        character.draw(screen)

        font = pygame.font.Font(
            None,
            32
        )

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

        blocks_text = font.render(
            f"Blocks remaining: {len(blocks)}",
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

        screen.blit(
            blocks_text,
            (20, 90)
        )

    # Win screen
    elif game_state == GAME_FINISHED:

        font_big = pygame.font.Font(
            None,
            70
        )

        font = pygame.font.Font(
            None,
            35
        )

        title = font_big.render(
            "GEFELICITEERD!",
            True,
            (255, 220, 50)
        )

        message = font.render(
            "Je hebt alle blokken gebroken!",
            True,
            (255, 255, 255)
        )

        instruction = font.render(
            "Sluit het venster om het spel te beëindigen.",
            True,
            (180, 180, 180)
        )

        screen.blit(
            title,
            (
                SCREEN_WIDTH // 2 - title.get_width() // 2,
                170
            )
        )

        screen.blit(
            message,
            (
                SCREEN_WIDTH // 2 - message.get_width() // 2,
                280
            )
        )

        screen.blit(
            instruction,
            (
                SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                350
            )
        )

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

    cv2.imshow(
        "Camera - AI Gesture Recognition",
        frame
    )

    previous_gesture = gesture

    pygame.display.flip()

    clock.tick(60)

camera.release()

cv2.destroyAllWindows()

hands.close()

pygame.quit()
