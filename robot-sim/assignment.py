from __future__ import print_function
import time
from sr.robot import *



a_th = 0.5  # angle threshold
d_th = 0.4 # distance threshold
d_th1 = 0.6
paired_boxes = set()  # A set to store paired golden boxes



R = Robot()



def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def SearchToken1(code,pair):
    if pair==1: #Search4NewToken()
        code = None
        dist = 100
        for token in R.see():
            if token.dist < dist and token.info.code not in paired_boxes:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code
           
        if dist == 100:
            return -1, -1, None
        else:
            return dist, rot_y, code

    elif pair == True: #SearchpairedToken()
        dist = 100
        for token in R.see():
                if token.dist < dist and token.info.code in paired_boxes:
                    dist = token.dist
                    rot_y = token.rot_y
                    code = token.info.code   
        if dist == 100:
            return -1, -1, None
        else:
            return dist, rot_y, code


    elif pair == False: #SearchToken(code)
        dist = 100
        for token in R.see():
            if token.info.code == code:
                if token.dist < dist:
                    dist = token.dist
                    rot_y = token.rot_y
                    code = token.info.code
                    print("rot_y", rot_y)   
        if dist == 100:
            return -1, -1, None
        else:
            return dist, rot_y, code



def reach_token1(code,handle, pair):
    var = True
    while var:
        dist, rot_y,code = SearchToken1(code,pair) # we look for markers
        if dist == -1:
            print("I don't see",code," token!!")
            turn(10, 1)  # if no markers are detected, the program ends
        elif dist < d_th1 and handle==True or dist < d_th and handle==False:
            print("Found",code) 
            var = False                                         
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left
            print("Left a bit...",code)
            turn(-2, 0.001)
        elif rot_y > a_th:  # if the robot is not well aligned with the token, we move it on the right
            print("Right a bit...",code)
            turn(+2, 0.001)
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!",code)
            drive(100, 0.1)

def BringToken_i_2_1(code,code1):
    handle=False
    pair=False
    reach_token1(code,handle, pair) 
    R.grab()
    handle=True
    print("Gotcha!")
    pair=True
    reach_token1(code1,handle, pair)
    R.release()
    paired_boxes.add(code)
    print("Released!")
    drive(-100, 0.5)


def main():
    var1=True
    time=0
    code1=None
    while var1 :
        time=0
        if code1 == None :
            pair=1
            dist1, rot_y1, code1 = SearchToken1(code1,pair)
            paired_boxes.add(code1)
            print("code1", code1)
            var1=False
            var2=True
            while var2:
                code=None
                pair=1
                dist, rot_y, code = SearchToken1(code,pair)
                print("code", code)
                if code != None:
                    time=0
                    pair=True
                    dist1, rot_y1, code1 = SearchToken1(code1,pair)
                    BringToken_i_2_1(code,code1)
                elif code == None:
                    print("I don't see any token!!")
                    turn(10, 1)
                    time=time+1
                    if time==20:
                        print("all token are paired click esc to close")
                        exit()
        elif time<20:
            print("I don't see any token!!")
            turn(10, 1)  # if no markers are detected, the program ends
            time=time+1
            if time==20:
                print("there are no token")
                exit()


main()