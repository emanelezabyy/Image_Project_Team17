#include <Servo.h>

Servo servoMotor;

char command;

void setup() {

  Serial.begin(9600);      // Start serial communication
  servoMotor.attach(9);    // Servo signal pin connected to Arduino pin 9

}

void loop() {

  if (Serial.available()) {

    command = Serial.read();

    if (command == 'C') {
      servoMotor.write(70);   // Rotate clockwise
    }

    else if (command == 'A') {
      servoMotor.write(110);  // Rotate counter-clockwise
    }

    else if (command == 'F') {
      servoMotor.write(60);   // Faster clockwise
    }

    else {
      servoMotor.write(90);   // Stop servo
    }

  }

}
