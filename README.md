# AssistAI Robot

![AssistAI](https://placehold.co/800x400/2A303C/FFFFFF?text=AssistAI%20Robot)

**AssistAI** is a smart, interactive voice assistant built to run on a Raspberry Pi 4B. It features facial recognition to greet users by name, bilingual (English and Bengali) conversational abilities, and an animated face for expressive interactions.

This project combines hardware and software to create a friendly, helpful companion robot. It's designed to be modular and extensible, making it a great platform for further development in robotics and artificial intelligence.

## ✨ Features

* **Facial Recognition:** Recognizes known users and greets them personally using a pre-trained OpenCV model.
* **Bilingual Conversation:** Seamlessly communicates in both **English** and **Bengali**, with the ability to switch languages on command.
* **Gemini-Powered Intelligence:** Utilizes the Google Gemini API for advanced question-answering and conversational context.
* **Animated Face:** Displays dynamic animations on a screen for different states (idle, listening, thinking, talking) to provide visual feedback.
* **Smart Acknowledgement:** Provides instant feedback when a complex question is asked, improving the user experience by eliminating awkward silences.
* **Interruptible Speech:** The robot can be interrupted mid-sentence with a stop command.
* **Servo Control:** Integrates with an Arduino to control servos for physical gestures like waving and thinking.
* **Modular Codebase:** The project is organized into logical modules for easy understanding and modification.

## 🛠️ Hardware Requirements

* **Raspberry Pi:** Raspberry Pi 4 Model B (2GB or higher recommended)
* **Microphone:** A USB microphone for voice input.
* **Speaker:** Any standard speaker with a 3.5mm jack or USB connection.
* **Camera:** Raspberry Pi Camera Module or a standard USB webcam.
* **Display:** A small screen compatible with the Raspberry Pi (e.g., a 3.5" or 5" SPI/HDMI display) to show the animated face.
* **Arduino:** An Arduino board (e.g., Uno, Nano) to control the servos.
* **Servos:** Standard servo motors for physical movements.

## ⚙️ Software & Installation

### 1. Prerequisites

* A fresh installation of Raspberry Pi OS.
* Python 3.7 or higher.
* Arduino IDE to upload the sketch to the Arduino board.

### 2. Clone the Repository

Open a terminal on your Raspberry Pi and clone this repository:

```bash
git clone [https://github.com/GoutomRoy64/AssistAI_Robot_With_RaspberryPi.git](https://github.com/GoutomRoy64/AssistAI_Robot_With_RaspberryPi.git)
```

### 3. Install Python Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

*(You will need to create a `requirements.txt` file with the following content):*



### 4. Set Up Google Gemini API Key

Your Gemini API key must be kept secure and should not be hardcoded.

1.  Create a file named `.env` in the main project directory:
    ```bash
    nano .env
    ```
2.  Add your API key to this file:
    ```
    GEMINI_API_KEY="AIzaSy...Your...Key"
    ```
3.  Save the file (`Ctrl+X`, `Y`, `Enter`). The `AI_Handler.py` script is already set up to load this key securely.

### 5. Upload Code to Arduino

1.  Open the `Hardware/Arduino_Code/AssistAI_Servos.ino` sketch in the Arduino IDE.
2.  Connect your Arduino Uno to your computer.
3.  Select the correct board and port from the `Tools` menu.
4.  Click the "Upload" button to flash the code to the Arduino.

### 6. Capture Faces for Recognition

To recognize you, the robot needs pictures of your face.

1.  Create a directory for your face inside `known_faces/`:
    ```bash
    mkdir -p known_faces/YourName
    ```
    (Replace `YourName` with your actual name, no spaces).

2.  Run the `capture_faces.py` script. You may need to edit the script to set `person_name` to your name.
    ```bash
    python Software/capture_faces.py
    ```
3.  Look at the camera. The script will save 20 images of your face and then quit.

### 7. Train the Face Recognition Model

After capturing faces, you need to train the model. The main script does this automatically if a model doesn't exist, but you can also run the training process manually by adapting the `train()` method in `Face_Recognition.py`.

## 🚀 Usage

To start the robot, run the main script from the project's root directory:

```bash
python AssistAI_robot.py
```

The robot will:
1.  Initialize and check for a trained face model.
2.  Attempt to recognize a face.
3.  Greet the user and begin listening for commands in Bengali.

You can say "change to English" to switch the language.

## 📂 Project Structure

```
AssistAI-RaspberryPi/
│
├── AssistAI_robot.py       # The main application entry point and state machine.
├── README.md               # This file.
├── requirements.txt        # List of Python dependencies.
├── .env                    # Secure file for API keys (you must create this).
│
├── Hardware/Arduino_Code/          
│   └── AssistAI_Servos.ino   # Folder for the Arduino sketch.
│
├── known_faces/            # Directory to store face images for training.
│   └── YourName/
│       └── 1.jpg, 2.jpg...
│
└── Software/
    ├── AI_Handler.py           # Manages interaction with the Google Gemini API.
    ├── Animation_Player.py     # Manages loading and displaying face animations.
    ├── Face_Display.py         # Handles the Pygame display thread.
    ├── Face_Recognition.py     # Handles face detection, training, and recognition.
    ├── Language_Manager.py     # Manages language state (EN/BN).
    ├── Response_Generator.py   # Generates responses (simple and AI-powered).
    ├── Servo.py                # Handles communication with the Arduino for servo control.
    ├── Speech_Listener.py      # Manages non-blocking speech recognition.
    ├── Tts_Player.py           # Handles Text-to-Speech conversion and playback.
    └── Units.py                # Utility functions.
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/GoutomRoy64/AssistAI_Robot_With_RaspberryPi/issues).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

A special thanks to the open-source community for the powerful libraries that made this project possible.
