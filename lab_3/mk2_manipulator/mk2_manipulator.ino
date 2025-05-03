#include <Servo.h>

Servo q0_servo;
Servo q1_servo;
Servo q2_servo;

String inputString = "";
bool stringComplete = false;

int q0_pos = 90;
int q1_pos = 90;
int q2_pos = 90;
int q1_off = 5;
int q2_off = 10;


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void setup() {
  // use monitoring with serial
  Serial.begin(115200);
  q0_servo.attach(3);
  q1_servo.attach(5);
  q2_servo.attach(6);
  delay(20);
  // set the servo to the home position
  q0_servo.write(90);
  delay(20);
  q1_servo.write(90+q1_off);
  delay(20);
  q2_servo.write(90+q2_off);
  delay(20);
}

void loop() {

  if (stringComplete) {
    Serial.println(inputString);
    if (inputString.substring(0, 1) == "T") {
      q0_pos = inputString.substring(1, 4).toInt();
      q1_pos = inputString.substring(4, 7).toInt();
      q2_pos = inputString.substring(7, 10).toInt();
      q1_pos = q1_pos+q1_off;
      q2_pos = q2_pos+q2_off;
      q0_servo.write(q0_pos);
      q1_servo.write(q1_pos);
      q2_servo.write(q2_pos);
      inputString = "";
      stringComplete = false;
    }
    inputString = "";
    stringComplete = false;
  }
}