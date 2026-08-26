import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kan de webcam niet openen.")
    exit()

while True:
    success, frame = camera.read()

    if not success:
        print("Kan geen beeld van de webcam lezen.")
        break

    cv2.imshow("Webcam", frame)

    # Druk op Q om af te sluiten
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()