<p align="center">
  <img src="https://github.com/AnuronDutta/PosturePro/assets/62471257/c2cebcf1-dac9-4519-b4b7-3bf7c5c23dc3" alt="Logo" height=200></a>
</p>

# PosturePro: Posture Monitoring App



## Overview

PosturePro is a posture monitoring application designed to help you maintain a healthy posture. This distribution includes the executable file (`PosturePro.exe`) for easy installation and usage.

## Features

- **Real-time Posture Monitoring**: PosturePro continuously tracks your body's key landmarks to evaluate your posture.

- **Perfect Posture Calibration**: Set your perfect posture angle by pressing 'P' when you're in an ideal position. The application will then monitor and provide feedback based on this reference angle.

- **Adjustable Thresholds**: Customize the sensitivity of the posture monitoring system by adjusting the deviation angle and time thresholds.

- **Posture Alerts**: Receive visual and audible alerts if your posture deviates significantly from the calibrated perfect posture for an extended duration.

- **Customizable sound alerts**: Change the sound alert to whatever you want by following instructions in the "Customizing Sound Alerts" section.

- **Pause/Resume Video Feed**: Conveniently pause and resume the video feed using the 'Esc' key, allowing you to temporarily disable posture monitoring.

## Controls

- **'P' Key**: Set or reset your perfect posture angle. Press 'P' again to re-record when needed.

- **'Esc' Key**: Toggle pause and resume for the video feed. Useful when you need a break from posture monitoring.

- **'I' and 'O' Keys**: Adjust the deviation angle threshold. Press 'I' to decrease and 'O' to increase.

- **'K' and 'L' Keys**: Adjust the time threshold for posture alerts. Press 'K' to decrease and 'L' to increase.

- **'Q' Key**: Quit the application.

## How To Use

**Calibrate Your Perfect Posture:**

- Upon opening the app, move into your preferred position and press 'P' to record it.
- Leave the program running in the background as you continue your work.

**Receive Posture Alerts:**

- The app will monitor your posture and provide visual and audio alerts when it deviates from the recorded position beyond a specific angle and time threshold.
- These alerts will remind you to correct your posture.

**Monitor Key Parameters:**

- The recorded perfect posture angle, deviation angle threshold, and time threshold are displayed in the top right corner of the app.

**Pause and Adjust Settings:**

- Press 'Esc' to pause the video feed temporarily.
- Use the following keys to adjust settings:
  - 'I': Decrease deviation angle threshold
  - 'O': Increase deviation angle threshold
  - 'K': Decrease time threshold
  - 'L': Increase time threshold

**Exit the Application:**

- Press 'Q' or manually close the window to exit the application.
## Getting Started

1. **Download**: Download the `PosturePro.exe` file from the release section.

2. **Run the Application**:
   - Double-click on `PosturePro.exe` to launch the application.

3. **Calibrate Perfect Posture**:
   - Follow on-screen instructions to set your perfect posture angle by pressing 'P'.

4. **Adjust Thresholds (Optional)**:
   - Fine-tune the monitoring sensitivity using the 'I', 'O', 'K', and 'L' keys.

## Customizing Sound Alerts
**To change the sound alert:**

1. Download a preferred sound effect in .WAV format.
   
2. Rename the downloaded file to `sound.wav`.

3. Locate the `sound.wav` file in the root directory of the application (where the `PosturePro.exe` file is located).

4. Replace the existing `sound.wav` file with your preferred one.

## Notes

- For optimal results, ensure good lighting conditions and a clear view of your body's landmarks.

- The application uses the MediaPipe Pose library, which may have limitations in extreme poses or low-light environments.

- Customize the application settings based on your preferences and comfort level.

## Troubleshooting

- If issues persist, please refer to the relevant documentation for:
  - [OpenCV](https://docs.opencv.org/4.x/index.html)
  - [MediaPipe](https://mediapipe.dev/)


Enjoy better posture with PosturePro!
