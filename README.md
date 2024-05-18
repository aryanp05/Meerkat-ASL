# Meerkat ASL

**Meerkat ASL** is a project aimed at building an American Sign Language (ASL) recognition system using computer vision techniques and machine learning algorithms. Meerkat ASL allows users to capture their own data for ASL by simply showing their camera the hand sign and typing the associated word. Meerkat will use the user data to then train itself in order to recognize the hand gesture and output it. Meerkat ASL also allows users to make fine tuning adjustments to the AI model through a testing mode, which allows users to use their camera to correct the AI if it produces an incorrect output for hand gesture at a specific angle or height. Meerkat ASL also comes with a easy to navigate GUI and allows users to learn any keybinds needed to utlize the machine.

## Features

- **ASL Recognition**: The system can recognize American Sign Language gestures in real-time using computer vision.
- **Capture Mode**: Allows users to capture images of ASL gestures for training and testing purposes.
- **Testing Mode**: Enables users to test the ASL recognition system by inputting ASL gestures and receiving predictions.
- **Training Mode**: Trains the machine learning model using captured ASL gesture data.

## Getting Started

To get started with Meerkat ASL, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run `Meerkat_Main.py` to launch the application.

## Usage

1. **ASL Mode**: Launches the application in ASL recognition mode, where the system recognizes ASL gestures in real-time.
2. **Capture Mode**: Allows users to capture images of ASL gestures for training and testing purposes.
3. **Testing Mode**: Enables users to test the ASL recognition system by inputting ASL gestures and receiving predictions.
4. **Training Mode**: Trains the machine learning model using captured ASL gesture data.

## Dependencies

- Python 3.x
- OpenCV
- Mediapipe
- Scikit-learn
- Numpy

## Contributing

Contributions are welcome! If you'd like to contribute to Meerkat ASL, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
