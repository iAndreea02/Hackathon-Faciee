import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera nu poate fi pornita!")
    exit()

WINDOW_NAME = "Camera Test"
cv2.namedWindow(WINDOW_NAME)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nu mai pot citi frame-uri de la camera.")
        break

    cv2.imshow(WINDOW_NAME, frame)

    # Citim tastele
    key = cv2.waitKey(1)

    # Apasat Q sau ESC
    if key == ord('q') or key == 27:
        break

    # Fereastra a fost închisă manual
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

