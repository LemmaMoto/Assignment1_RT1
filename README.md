Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 or Python 3 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash
$ python3 run.py <file_name>
```

# Token Handling Robot

This Python program is designed to simulate a robot that can locate, pick up, and pair tokens in a simple arena. The robot is equipped with a set of functions to control its movement, grab and release tokens, and identify the tokens and their pairings. The program is created for a Python Robotics Simulator and uses the Student Robotics API.

## Program Overview

The program is intended to operate within a simulated environment using a Python Robotics Simulator. It simulates a robot capable of the following tasks:

1. **Token Detection:** The robot scans its environment for tokens. It identifies unpaired tokens and searches for their paired counterparts.

2. **Token Pairing:** The robot pairs unpaired tokens with their corresponding tokens.

3. **Movement Control:** It can move forward, turn, and stop as needed to reach and manipulate tokens.

## How to Run

1. **Prerequisites:**

    - **Python:** Ensure you have Python installed on your system.
    - **Python Robotics Simulator:** You should have the Python Robotics Simulator installed.

2. **Running the Program:**

    Execute the program using the Python Robotics Simulator with the following command:

    ```bash
    python3 run.py <your-script>.py
    ```

    Replace `<your-script>` with the name `assignment` to run the simulation.

## Program Structure

- `run.py`: Entry point to run the program using the Python Robotics Simulator.

- `assignment.py`: Contains the main robot control functions for movement, token detection, pairing, and more.

- `assignment_more_readable.py`: Contains a more readable solution that works exactly the same as `assignment.py` but i didn't had time to rewrite the pseudo-code and to comment the parts I cropped up.


## Program Flow
# Token Handling Robot Pseudocode

## Initialize the robot
- Initialize robot

## Set distance and angle thresholds
- Set distance and angle thresholds

## Create an empty set to store paired tokens
- Create an empty set to store paired tokens

## Function to drive for a given time
- Define function to drive for a given time
   Set motor power to speed
   Wait for seconds
   Set motor power to 0

## Function to turn for a given time
- Define function to turn for a given time
   Set motor power for the left motor to speed
   Set motor power for the right motor to -speed
   Wait for seconds
   Set motor power for both motors to 0

## Function to search for a new token
- Define function to search for a new token
   Set NewToken to None
   Set dist to 100
   For each token seen by the robot:
    - If the token is not paired and closer than the current closest token:
       Set dist to the distance to the token
       Set NewToken to the code of the token
  - If no unpaired token is found:
     Return None
  - Else:
     Return the code of the closest unpaired token

## Function to search for a paired token
- Define function to search for a paired token
   Set PairedToken to None
   Set dist to 100
   For each token seen by the robot:
    - If the token is paired and closer than the current closest token:
       Set dist to the distance to the token
       Set PairedToken to the code of the token
  - If no paired token is found:
     Return None
  - Else:
     Return the code of the closest paired token

## Function to search for a token with a given code
- Define function to search for a token with a given code
   Set dist to 100
   For each token seen by the robot:
    - If the token has the given code and closer than the current closest token:
       Set dist to the distance to the token
       Set rot_y to the rotation angle to the token
  - If no token with the given code is found:
     Return -1, -1
  - Else:
     Return the distance and rotation angle to the closest token with the given code

## Function to reach a token with a given code
- Define function to reach a token with a given code
   Print a message indicating that the robot is looking for the token
   Set var to True
   While var is True:
     Search for the token with the given code
    - If the token is not found:
       Print a message indicating that the token cannot be found
       Turn the robot to search for the token
    - Else if the token is close enough to be grabbed and the robot is not already handling a token:
       Print a message indicating that the token is found
       Set var to False
    - Else if the robot is not well aligned with the token:
       Turn the robot to align with the token
    - Else if the robot is well aligned with the token:
       Drive the robot forward

## Function to bring an unpaired token to a paired token
- Define function to bring an unpaired token to a paired token
   Set handle to False
   Reach the unpaired token with the given code
   Grab the token
   Set handle to True
   Print a message indicating that the robot is bringing the unpaired token to the paired token
   Reach the paired token with the given code
   Release the token
   Add the unpaired token to the set of paired tokens
   Print a message indicating that the token is released
   Drive the robot backward

## Main function to bring all tokens to one place near the first token seen
- Define the main function
   Set time to 0
   Set FindFirstToken to True
   Set FirstToken to None
  - While FindFirstToken is True:
    - If the first token is not found:
       Search for the first token
      - If the first token is found:
         Add it to the set of paired tokens
         Set FindFirstToken to False
         Set FindUnpairedToken to True
        - While FindUnpairedToken is True:
           Search for an unpaired token
          - If an unpaired token is found:
             Set time to 0
             Set FindUnpairedToken to False
             Set FindPairedToken to True
            - While FindPairedToken is True:
               Search for a paired token
              - If a paired token is found:
                 Set time to 0
                 Bring the unpaired token to the paired token
                 Set FindPairedToken to False
                 Set FindUnpairedToken to True
              - Else if no paired token is found:
                 Print a message indicating that no paired token is found
                 Turn the robot to search for a paired token
                 Increment time
                - If time reaches 20 seconds:
                   Print a message indicating that all tokens are not paired
                   Exit the program
          - Else if no unpaired token is found:
             Print a message indicating that no token is found
             Turn the robot to search for a token
             Increment time
            - If time reaches 20 seconds:
               Print a message indicating that all tokens are paired
               Exit the program
    - Else if the first token is not found for 20 seconds:
       Print a message indicating that no token is found
       Turn the robot to search for a token
       Increment time
      - If time reaches 20 seconds:
         Print a message indicating that there are no tokens

## Call the main function
- Call the main function


## Customization

You can customize the program by adjusting the threshold values for distance and angle (`a_th`, `d_th`, `d_th_2_pair`) and by modifying the robot's behavior based on your specific requirements.

## Possible Improvements

- Implement additional error handling and recovery mechanisms to handle unexpected situations effectively.
- Integrate more advanced path planning and obstacle avoidance algorithms to improve the robot's efficiency.
- Enhance the visual feedback to provide a more detailed view of the robot's surroundings.
- Consider additional functionalities such as token ordering, more complex token manipulation, or real-time monitoring.

## License

This program is open-source and available under the [MIT License](LICENSE). Feel free to modify and use it for your projects.

## Acknowledgments

This program was developed with the help of the Python Robotics Simulator and the Student Robotics API.

---

Feel free to add any additional details, dependencies, or acknowledgments specific to your environment or use case. This README provides a general structure to get you started.


You have also the solutions of the exercises (folder solutions)



Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
