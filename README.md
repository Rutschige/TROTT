# TROTT
The Robotic Object Tracking Turret

### The final project submission for COSC 4364 developed by:
* Grant Williams
* Tyler Driver
* Sanaz Farhadi
* Sebastian Macedonio

### Project Details:
TROTT will receive an image input within a predetermined frame, identify the object, and once the object is moved and another image frame is received will then move the laser turret to the center of the object's new position

The purpose of this project is to showcase concepts from Numerical Methods, those being the following:
* Errors
  * Being able to detect the correct object and ignore noise
  * Only being able to detect objects within the given frame
* Equations
  * Image processing algorithm to detect object (DFT/FFT)
  * Algorithm for translating (x, y) coordinates into degrees for servo rotation
* Optimization
  * Improving the efficiency of the DFT/FFT algorithm
  * Setting interval of image update to be reasonable but not overload Arduino with data

### Instruction to Run the Project:
* Firstly, run the turret calibration method with the camera on to find the best physical location for the project and set a workable frame
* Second, place the object to track within the frame with nothing else in it, then run the initial FFT identification portion
* Then move the object within the frame and run the entire series of programs (FFT then pass to location to Arduino) to have TROTT update the laser's position
* Repeat the previous two steps until satisfied
