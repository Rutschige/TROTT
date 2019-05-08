#include <Servo.h>

bool initialize;

double pan;
double tilt;

Servo servoX;
Servo servoY;

int pos = 0;    // variable to store the servo position

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servoX.attach(10); 
  servoY.attach(11);
  servoX.write(90);
   delay(30);
  servoY.write(90);
  initialize = true;
  
}

void loop() {
  // put your main code here, to run repeatedly
  while(initialize) //This will run until the python program finishes calibration
  {//This code will draw the frame
    delay(800);
    servoX.write(70);
    delay(800);
    servoY.write(75);
    delay(800);
    servoX.write(110);
    delay(800);
   servoY.write(105);
   if(Serial.available()>0 && Serial.readStringUntil('\n') == "stop")
    initialize=false;
  }

  if(Serial.available()>0)
    {
      pan=Serial.readStringUntil('\n').toFloat(); //reads in the first value sent as pan
      servoX.write(pan); //writes the value to the pan servo
      while(Serial.available()==0); //waits for the arduino to recieve the next input
      tilt=Serial.readStringUntil('\n').toFloat(); //reads the second input as tilt
      servoX.write(tilt); //writes the value to the tilt servo
      Serial.println("continue"); //This string could be anything. The python program just waits for results
    }
    
}
