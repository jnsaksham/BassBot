//Include the Arduino Stepper Library
#include <AccelStepper.h>
//#include <LiquidCrystal_I2C.h> // Library for LCD

const int dirPin = 2;
const int stepPin = 3;


#define motorInterfaceType 1
AccelStepper plateStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  Serial.begin(9600);
  plateStepper.setMaxSpeed(5000);
  plateStepper.setAcceleration(30);

}

void loop () {


  plateStepper.setSpeed(2500); // use negative for clockwise, and positive for anticlockwise
  plateStepper.runSpeed();

}
