"""
Step 2: Basic Servo Movement Script

Uses the cvzone library to send in angles to your arduino board for
the 3 servos motors

install the pyserial lib as well
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


# ------------------- Main Loop -------------------

# Infinite loop to continuously demonstrate servo movements
target_positions = [90, 90, 90]  # Set target positions for LServo, RServo, and HServo
move_servo(target_positions)