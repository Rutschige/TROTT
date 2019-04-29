#include <Servo.h>

Servo servoX;
Servo servoY;

int pos = 0;    // variable to store the servo position

void setup() {
  // put your setup code here, to run once:
  servoX.attach(10); 
  servoY.attach(11);
  servoX.write(90);
   delay(30);
  servoY.write(90);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //This code will draw the frame
//  delay(800);
//  servoX.write(70);
//  delay(800);
//  servoY.write(75);
//  delay(800);
//  servoX.write(110);
//  delay(800);
//  servoY.write(105);
}
