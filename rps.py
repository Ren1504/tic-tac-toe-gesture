import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

capture = cv2.VideoCapture(0)


capture.set(3,640)
capture.set(4,480)

detector = HandDetector(maxHands = 1, detectionCon=0.7)

timer = 1
current = False
game = False
player = ""

state = 0

p = 0
cpu = 0

choices = ["rock","paper","scissors"]

while True:

    bg = cv2.imread("rsrcs/background.png")
    _, img = capture.read()



    scaled = cv2.resize(img,(0,0),None,0.75,0.75)
    scaled = scaled[:,120:480]


    hands, img = detector.findHands(scaled)

    if game:

        if current is False:
            timer = time.time() - initial
            cv2.putText(bg,str(int(timer)),(600,430),cv2.FONT_HERSHEY_PLAIN,6,(255,0,0),4)

            if timer > 3:
                current = True
                timer = 0

                if hands:
                    hand = hands[0] #take the first hand

                    fingers = detector.fingersUp(hand) #how many fingers are up

                    if fingers == [0]*5:
                        player = "rock"

                    if fingers == [1]*5:
                        player = "paper"

                    if fingers == [0, 1, 1, 0, 0]:
                        player = "scissors"

                    AIchoice = random.choice(choices)

                    AI = cv2.imread(f"rsrcs/{AIchoice}.png",cv2.IMREAD_UNCHANGED)

                    if(player == AIchoice):
                        state = 0
                    
                    if((player == "rock" and AIchoice == "scissors") or 
                       (player == "scissors" and AIchoice == "paper") or 
                       (player == "paper" and AIchoice == "rock")):
                        
                        state = 1
                        p+=1
                        #  cv2.putText(bg,"YOU WIN!",(575,200),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)

                    if((AIchoice == "rock" and player == "scissors") or
                       (AIchoice == "scissors" and player == "paper") or
                       (AIchoice == "paper" and player == "rock")):
                        
                        state = 2
                        cpu+=1
                    
                    # 900,380

                    print("player: ",player)
                    print("AI: ",AIchoice)
                    print("state: ",state)
    if current:
        bg = cvzone.overlayPNG(bg,AI,(900,220))

        if state == 1:
            cv2.putText(bg,"YOU WIN!",(400,200),cv2.FONT_HERSHEY_PLAIN,7,(255,0,0),2)

        if state == 0:    
            cv2.putText(bg,"DRAW!",(400,200),cv2.FONT_HERSHEY_PLAIN,7,(255,0,0),2)

        if state == 2:
            cv2.putText(bg,"CPU WIN!",(400,200),cv2.FONT_HERSHEY_PLAIN,7,(255,0,0),2)



    bg[210:570,53:413] = scaled

    cv2.putText(bg,str(p),(450,420),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),2)
    cv2.putText(bg,str(cpu),(740,420),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),2)

    cv2.imshow("GAME",bg)

    if cv2.waitKey(1) == ord('s'):
        game = True
        initial = time.time()
        current = False

    if cv2.waitKey(1) == ord('q'):
        break