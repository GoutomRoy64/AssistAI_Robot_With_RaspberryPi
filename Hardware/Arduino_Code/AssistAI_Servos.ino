// Include the Servo library to control servo motors
#include <Servo.h>

// --- Configuration ---
// Create servo objects for the robot's left and right hands.
Servo rightHandServo;
Servo leftHandServo;

// Define the pins your servos are connected to on the Arduino.
const int RIGHT_HAND_SERVO_PIN = 9;
const int LEFT_HAND_SERVO_PIN = 10;

// --- Main Program ---

void setup() {
  // Start the serial communication at 9600 bits per second (baud rate).
  // This must match the BAUD_RATE in your Python Servo.py file.
  Serial.begin(9600);
  
  // Attach the servo objects to their physical pins on the Arduino.
  rightHandServo.attach(RIGHT_HAND_SERVO_PIN);
  leftHandServo.attach(LEFT_HAND_SERVO_PIN);
  
  // Move both servos to a neutral starting position (90 degrees).
  rightHandServo.write(90);
  leftHandServo.write(90);
  
  Serial.println("Arduino is ready to receive commands.");
}

void loop() {
  // Check if there is any data available to read from the serial port.
  if (Serial.available() > 0) {
    // Read the incoming command from the serial port until a newline character is received.
    String command = Serial.readStringUntil('\n');
    
    // Trim any leading/trailing whitespace from the command.
    command.trim();

    // --- Command Handling ---
    // Check the received command and call the corresponding function.
    if (command.equalsIgnoreCase("WAVE")) {
      wave();
    } else if (command.equalsIgnoreCase("POINT_LEFT")) {
      pointLeft();
    } else if (command.equalsIgnoreCase("THINK")) {
      think();
    } else if (command.equalsIgnoreCase("CELEBRATE")) {
      celebrate();
    } else {
      // If the command is not recognized, print an error message.
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

// --- Gesture Functions ---

/**
 * @brief Performs a waving gesture with the right hand.
 */
void wave() {
  Serial.println("Executing: WAVE");
  // The left hand can stay neutral while the right hand waves.
  for (int i = 0; i < 3; i++) {
    rightHandServo.write(130); // Move to one side
    delay(300);
    rightHandServo.write(50);  // Move to the other side
    delay(300);
  }
  rightHandServo.write(90); // Return to neutral position
}

/**
 * @brief Points the left hand to the left.
 * The right hand remains in a neutral position.
 */
void pointLeft() {
  Serial.println("Executing: POINT_LEFT");
  // Note: The angle for the left servo might be mirrored.
  // If 160 degrees points "out" for the right hand, 20 might point "out" for the left.
  leftHandServo.write(20); // Angle for pointing left
  delay(1500);           // Hold the position
  leftHandServo.write(90); // Return to neutral position
}

/**
 * @brief Performs a "thinking" gesture with the right hand.
 * The left hand stays neutral.
 */
void think() {
  Serial.println("Executing: THINK");
  rightHandServo.write(45); // Move to a thoughtful position
  delay(2000);              // Hold the position
  rightHandServo.write(90); // Return to neutral
}

/**
 * @brief Performs a celebratory gesture with both hands.
 * A quick, energetic movement.
 */
void celebrate() {
  Serial.println("Executing: CELEBRATE");
  for (int i = 0; i < 2; i++) {
    // Both hands move up
    rightHandServo.write(180);
    leftHandServo.write(0);
    delay(200);
    // Both hands move down
    rightHandServo.write(90);
    leftHandServo.write(90);
    delay(200);
  }
}