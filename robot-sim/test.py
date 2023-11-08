from __future__ import print_function
import time
from sr.robot import *

# Thresholds for distance and angle
a_th = 0.5  
d_th = 0.4 
d_th_2_pair = 0.6 

# A set to store paired golden boxes
paired_boxes = set()  

# Initialize the robot
R = Robot()

# Function to drive for a given time
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds) 
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to turn for a given time
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to search for a new token
def search_token(token_type, code=None):
    dist = 100
    found_token = None
    rot_y = None
    for token in R.see():
        if token_type == 'new' and token.dist < dist and token.info.code not in paired_boxes:
            dist = token.dist
            found_token = token.info.code
        elif token_type == 'paired' and token.dist < dist and token.info.code in paired_boxes:
            dist = token.dist
            found_token = token.info.code
        elif token_type == 'specific' and token.info.code == code and token.dist < dist:
            dist = token.dist
            found_token = token.info.code
            rot_y = token.rot_y
    if token_type == 'specific':
        return (dist, rot_y) if dist != 100 else (-1, -1)
    else:
        return found_token if dist != 100 else None

# Function to reach a token with a given code
def reach_token1(code,handle):
    print("I'm looking for Token",code)
    var = True
    while var: 
        dist, rot_y= search_token('specific', code) 
        if dist == -1:
            print("I can't see",code," token!!")
            turn(100, 0.01)  # if no markers are detected, the program ends
        elif dist < d_th_2_pair and handle==True or dist < d_th and handle==False:
            print("Found Token",code) 
            var = False                                         
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left
            print("Left a bit for Token",code)
            turn(-2, 0.001)
        elif rot_y > a_th:  # if the robot is not well aligned with the token, we move it on the right
            print("Right a bit for Token",code)
            turn(+2, 0.001)
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are, for Token",code)
            drive(100, 0.1)

# Function to bring a token with a given UnpairedToken to a given PairedToken
def BringToken_i_2_1(UnpairedToken,PairedToken):
    handle=False
    reach_token1(UnpairedToken,handle)  #we reach the unpaired token
    R.grab()
    handle=True
    print("Gotcha!")
    print("I'm going to bring",UnpairedToken,"to",PairedToken)
    reach_token1(PairedToken,handle) #we reach the paired token
    R.release()
    paired_boxes.add(UnpairedToken) #we add the unpaired token to the set of paired tokens
    print("Released!")
    drive(-100, 0.5)

# Main function to bring all tokens to one place near the first token seen
def main():
    while True:
        time = 0
        FindFirstToken = True
        FirstToken = None

        while FindFirstToken:
            if FirstToken is None:
                FirstToken = search_token('new')
                paired_boxes.add(FirstToken)
                print("FirstToken", FirstToken)
                FindFirstToken = False
                FindUnpairedToken = True

        while FindUnpairedToken:
            UnpairedToken = search_token('new')
            print("UnpairedToken", UnpairedToken)
            if UnpairedToken is not None:
                time = 0
                FindUnpairedToken = False
                FindPairedToken = True
            else:
                print("I don't see any token!!")
                turn(100, 0.1)
                time += 1
                if time == 20:
                    print("all token are paired click esc to close")
                    exit()

        while FindPairedToken:
            PairedToken = search_token('paired')
            print("PairedToken", PairedToken)
            if PairedToken is not None:
                print("PairedToken ", PairedToken)
                time = 0
                BringToken_i_2_1(UnpairedToken,PairedToken)
                FindPairedToken = False
                FindUnpairedToken = True
            else:
                print("I don't see any paired token!!")
                turn(-100, 0.1)
                time += 1
                if time == 20:
                    print("all token are not paired click esc to close")
                    FindPairedToken = False

# Call the main function
main()
