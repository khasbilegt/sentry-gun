#include <Servo.h>  //Used to control the Pan/Tilt Servos

#define SERVO1_PWM 10
#define SERVO2_PWM 9

#define servoDelay 1000

#define acceleratorRelayPin 2
#define fireRelayPin 3

#define fireDelay 1000

//These are the objects for each servo.
Servo servoTilt, servoPan;

byte indicator;                       // if 'a', continue, if 'z', idle
byte x100byte;                        // some bytes used during serial communication
byte x010byte;
byte x001byte;
byte y100byte;
byte y010byte;
byte y001byte;
byte fireByte;

//This is a character that will hold data from the Serial port.
int serialChar;
int tiltPosition = 150;
int panPosition = 90;
int fire = 0;

void setup() {
  servoTilt.attach(SERVO1_PWM);
  servoPan.attach(SERVO2_PWM);
  servoTilt.write(tiltPosition);
  servoPan.write(panPosition);
    delay(servoDelay);

  pinMode(acceleratorRelayPin, OUTPUT);
  pinMode(fireRelayPin, OUTPUT);
  digitalWrite(acceleratorRelayPin, HIGH);
  digitalWrite(fireRelayPin, HIGH);

  Serial.begin(57600);
}

void loop() {
//  if (Serial.available() > 0) {
//    indicator = Serial.read();
//    x100byte = Serial.read();         // read the message, byte by byte
//    x010byte = Serial.read();         //
//    x001byte = Serial.read();         //
//    y100byte = Serial.read();         //
//    y010byte = Serial.read();         //
//    y001byte = Serial.read();         //
//    fireByte = Serial.read();         //
//
//    panPosition = (100 * (int(x100byte) - 48)) + (10 * (int(x010byte) - 48)) + (int(x001byte) - 48);
//    tiltPosition = (100 * (int(y100byte) - 48)) + (10 * (int(y010byte) - 48)) + (int(y001byte) - 48);
//    fire = int(fireByte) - 48;
//  }

  if (fire == 1) {
    shoot();
  }

  servoTilt.write(int(tiltPosition));
  servoPan.write(int(panPosition));
  //  delay(servoDelay);
}

void shoot() {
  digitalWrite(fireRelayPin, LOW);
  delay(fireDelay);
  digitalWrite(fireRelayPin, HIGH);
}
