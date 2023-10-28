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


def Search4NewToken():
        code = None
        dist = 100
        for token in R.see():
            if token.dist < dist and token.info.code not in paired_boxes:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code
           
        if dist == 100:
            return None
        else:
            return code
def SearchpairedToken():    
    dist = 100
    code = None  # Inizializziamo code come None
    for token in R.see():
        if token.dist < dist and token.info.code in paired_boxes:
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    return code  # Restituisci il code trovato, che potrebbe essere None se nessun token abbinato è stato trovato


def SearchToken(code):
    dist = 100
    for token in R.see():
      if token.info.code == code:
        if token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y
            print("rot_y", rot_y)   
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y



def reach_token1(code,handle):
    print("I'm looking for",code)
    var = True
    while var:
        dist, rot_y= SearchToken(code) # we look for markers
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
    reach_token1(code,handle) 
    R.grab()
    handle=True
    print("Gotcha!")
    print("I'm going to bring",code,"to",code1)
    reach_token1(code1,handle)
    R.release()
    paired_boxes.add(code)
    print("Released!")
    drive(-100, 0.5)


def main():
    var1=True
    time=0
    first=None
    while var1 :
        time=0
        if first == None :
            first = Search4NewToken()
            paired_boxes.add(first)
            print("first", first)
            var1=False
            var2=True
            while var2:
                code=None
                code = Search4NewToken()
                print("code", code)
                if code != None:
                    time=0
                    var2=False
                    var3=True
                    while var3:
                        code1=None
                        code1 = SearchpairedToken()
                        print("code1", code1)
                        if code1 != None:
                            print("code1 qwertyuiowertyui", code1)
                            time=0
                            BringToken_i_2_1(code,code1)
                            var3=False
                            var2=True
                        elif code1 == None:
                            print("I don't see any paired token!!")
                            turn(100, 0.1)
                            time=time+1
                            if time==20:
                                print("all token are not paired click esc to close")
                                var3=False
                elif code == None:
                    print("I don't see any token!!")
                    turn(100, 0.1)
                    time=time+1
                    if time==20:
                        print("all token are paired click esc to close")
                        exit()
        elif time<20:
            print("I don't see any token!!")
            turn(100, 0.1)  # if no markers are detected, the program ends
            time=time+1
            if time==20:
                print("there are no token")
                exit()



main()
