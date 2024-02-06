import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)
x = []
y = []

text = ""
k = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

idset = ["", "1", "12", "123", "1234", "01234", "0", "01", "012", "0123", "04", "4", "34", "014", "14", "234"]
op = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-","*","/", "="]


while True:
    success, frame = cam.read()
    img = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape

                if id == 0:
                    x = []
                    y = []

                x.append(int((lm.x) * w))
                y.append(int((1 - lm.y) * h))

                if len(y) > 20:
                    gesture_id = ""
                    big = [x[3], y[8], y[12], y[16], y[20]]
                    small = [x[4], y[6], y[10], y[14], y[18]]

                    for _ in range(len(big)):
                        if big[_] > small[_]:
                            gesture_id += str(_)

                    k[idset.index(gesture_id)] += 1

                    for i in range(len(k)):
                        if k[i] > 20:
                            if i == 15:
                                ans = str(eval(text))
                                text = "=" + ans
                                for j in range(len(k)):
                                    k[j] = 0
                            else:
                                text += op[i]

                                for j in range(len(k)):
                                    k[j] = 0

            cv2.putText(img, text, (60, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 5)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
    else:
        text = " "

    cv2.imshow("Visual Calculator", img)
    
    if cv2.waitKey(10) & 0XFF==27:
         break

cv2.destroyAllWindows()
cam.release()
