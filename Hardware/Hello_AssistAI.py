"""
Hello Gesture

"""
# ------------------- Import Libraries -------------------

from cvzone.SerialModule import SerialObject  # Import the SerialObject for serial communication with Arduino
from time import sleep  # Import sleep to add delays between actions

# ------------------- Initializations -------------------

# Create a Serial object with three digits precision for sending servo angles
arduino = SerialObject(digits=9)

# Initialize the last known positions for the three servos: Left (LServo), Right (RServo), Head (HServo)
# LServo starts at 180 degrees, RServo at 0 degrees, and HServo at 90 degrees
last_positions = [180, 0, 90]
#                [LServo , RServo ,HServo ]

# ------------------- Functions -------------------

# Function to smoothly move servos to target positions
def move_servo(target_positions, delay=0.0001):
    """
    Moves the servos smoothly to the target positions.

    :param target_positions: List of target angles [LServo, RServo, HServo]
    :param delay: Time delay (in seconds) between each incremental step
    """
    global last_positions  # Use the global variable to track servo positions
    # Calculate the maximum number of steps required for the largest position difference
    max_steps = max(abs(target_positions[i] - last_positions[i]) for i in range(3))

    # Incrementally move each servo to its target position over multiple steps
    for step in range(max_steps):
        # Calculate the current position of each servo at this step
        current_positions = [
            last_positions[i] + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            if abs(target_positions[i] - last_positions[i]) > step else last_positions[i]
            for i in range(3)
        ]
        # Send the calculated positions to the Arduino
        arduino.sendData(current_positions)
        # Introduce a small delay to ensure smooth motion
        sleep(delay)

    # Update the last known positions to the target positions
    last_positions = target_positions[:]


def hello_gesture():
    """
    Makes Emma wave hello by moving the right servo back and forth.
    """
    global last_positions
    # Move right arm to start waving
    move_servo([last_positions[0], 180, last_positions[2]])
    for _ in range(3):  # Perform the waving motion 3 times
        move_servo([last_positions[0], 150, last_positions[2]])  # Move arm slightly down
        move_servo([last_positions[0], 180, last_positions[2]])  # Move arm back up
    # Reset arm to original position
    move_servo([last_positions[0], 0, last_positions[2]])

# ------------------- Main Loop -------------------

hello_gesture()