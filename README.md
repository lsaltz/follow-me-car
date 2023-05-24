# follow-me-car
 A car I designed in Fusion360 to follow me in an isolated area.
 
 # Software
- Python3
- OpenCV
- Waveshare motor controller code

# Hardware
- Jetson Nano Dev Kit
- Camera
- Waveshare Stepper Motor HAT (B)
- 2 Nema 17 Stepper Motors

# Design Process
The goal of this project is to use what I have to create something. I do not currently have any DC motors, so I chose to use steppers that I have had for a while. I have a Jetson Nano from a while ago, so I chose to use that. 
The only part I ordered for this was the motor controller, as I do not currently own any. The vehicle has a unique design where I chose to 3D print ball bearings and use them as wheels. The code uses OpenCV's HOG to detect me, and then KCF to track me.
