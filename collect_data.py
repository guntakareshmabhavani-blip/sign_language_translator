 #print("Test started")
import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Signs nuvvu collect cheయాలనుకుంటున్నావు
signs = {
    '1': 'Hello',
    '2': 'ThankYou',
    '3': 'Yes',
    '4': 'No',
    '5': 'Please'
}

print("Keys: 1=Hello 2=ThankYou 3=Yes 4=No 5=Please | s=Save sample | q=Quit")

# CSV file create cheయడం (లేకపోతే)
filename = 'hand_data.csv'
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['label']
        for i in range(21):
            header += [f'x{i}', f'y{i}', f'z{i}']
        writer.writerow(header)

current_sign = None
count = 0

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    landmark_list = None
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            landmark_list = []
            for lm in handLms.landmark:
                landmark_list += [lm.x, lm.y, lm.z]

    # Screen meeda current sign mరియు count chూపించడం
    text = f"Sign: {current_sign or 'None'} | Count: {count}"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif chr(key) in signs:
        current_sign = signs[chr(key)]
        count = 0
        print(f"Selected sign: {current_sign}")
    elif key == ord('s') and current_sign and landmark_list:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([current_sign] + landmark_list)
        count += 1
        print(f"Saved sample {count} for {current_sign}")

cap.release()
cv2.destroyAllWindows()
print("Data collection done. Check hand_data.csv")
