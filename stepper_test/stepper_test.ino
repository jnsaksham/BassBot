//Include the Arduino Stepper Library
#include <AccelStepper.h>
//#include <LiquidCrystal_I2C.h> // Library for LCD

const int dirPin = 2;
const int stepPin = 3;


#define motorInterfaceType 1
AccelStepper stepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(5000);
  // stepper.setAcceleration(30);

}

void loop () {


  stepper.setSpeed(2000); // use negative for clockwise, and positive for anticlockwise
  stepper.runSpeed();
  // delay(500);
  // Stop the motor from rotating
  stepper.stop();
  
  // Print current position
  // stepper.currentPosition();

  // Move n num_steps ahead

}
