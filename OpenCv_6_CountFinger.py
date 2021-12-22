import  cv2
import  time
import  os

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


pTime =0
cap = cv2.VideoCapture(0)
FolderPath ="Fingers";
lst_Finger = os.listdir(FolderPath);
lst_2 = [];
for i in lst_Finger:
    image = cv2.imread(f"{FolderPath}/{i}")
    print(f"{FolderPath}/{i}")
    lst_2.append(image)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    fingerid = [4,8,12,16,20]
    while cap.isOpened():
        ret, frame = cap.read();

        # Viet ra FPS
        cTime = time.time()
        fps = 1/(cTime-pTime);
        pTime = cTime

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        lmList = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
        # Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        if len(lmList) != 0:
            fingers = [];
            right  = True;
            # Viết cho ngón cái :
            if lmList[0][1] > lmList[1][1] : right = False;
            else: right = True;
            if right == True :
                if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                    fingers.append(0)
                else:
                    fingers.append(1)
            else:
                if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Viết cho ngón dài :
            for id in range(1,5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            print(fingers)
            countFinger = fingers.count(1);
            h, w, c = lst_2[countFinger-1].shape
            frame[0:h, 0:w] = lst_2[countFinger-1]
        # show fps len man hinh
        cv2.putText(frame , f"FPS: {int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.imshow("Cua so cam", frame);
        if (cv2.waitKey(1) == ord("q")): break
cap.release();
cv2.destroyAllWindows()