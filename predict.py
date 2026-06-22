import cv2
import mediapipe as mp
import pickle
import win32com.client

# Load trained model
with open('sign_model.pkl', 'rb') as f:
    model = pickle.load(f)

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

# Windows Voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")

last_prediction = ""

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            landmark_list = []

            for lm in handLms.landmark:
                landmark_list.extend([lm.x, lm.y, lm.z])

            prediction = str(model.predict([landmark_list])[0])

            cv2.putText(
                frame,
                prediction,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

            if prediction != last_prediction:
                print("Speaking:", prediction)

                try:
                    speaker.Speak(prediction)
                except Exception as e:
                    print("Voice Error:", e)

                last_prediction = prediction

    cv2.imshow("Sign Language Translator", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
