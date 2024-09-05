# follow-me-car
 A robotic vehicle I designed in Fusion360 to follow me in an isolated area.
 
 ## Software
- Python3
- OpenCV
- Waveshare motor controller code

## Hardware
- Jetson Nano Dev Kit
- Camera
- Waveshare Stepper Motor HAT (B)
- 2 Nema 17 Stepper Motors

## Design Process
The goal of this project is to use what I have to create something. I do not currently have any DC motors, so I chose to use steppers that I have had for a while. I have a Jetson Nano from a while ago, so I chose to use that. 
The only part I ordered for this was the motor controller, as I do not currently own any. The vehicle has a unique design where I chose to 3D print ball bearings and use them as wheels. The code uses OpenCV's HOG to detect me, and then KCF to track me.

## Project Summary
Overall the end result was a robot without wheels. The stepper motors I had did not have enough torque to drive the robot, even after I:
- reduced the weight
- increased the current
- reduced motor speed
- increased wheel traction

Ultimately, using OpenCV, the robot was able to detect and track me, and the motors moved accordingly.

## Moving Forward
If I were to take this project further, I would:
- Redesign chassis
- Get/design different wheels
- Change to higher torque motors
- Explore other options for person detection
- Incorporate a feature for scanning and remembering an individual on startup
- Look at parallel motor control options

## Sources
https://automaticaddison.com/how-to-detect-pedestrians-in-images-and-video-using-opencv/
