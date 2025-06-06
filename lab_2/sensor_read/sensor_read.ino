#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <ArduinoJson.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

#include <Encoder.h>

// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder myEnc(2, 3);
//   avoid using pins with LEDs attached

String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(115200);
  pinMode(13, INPUT_PULLUP);
  accel.setRange(ADXL345_RANGE_16_G);
  accel.begin();
  delay(100);
}

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

void loop() {

  if (!digitalRead(13)) {
    myEnc.write(1000);
  }
  if (stringComplete) {
    if (inputString.substring(0, 2) == "GO") {
      long newPosition = myEnc.read();
      /* Get a new sensor event */
      sensors_event_t event;
      accel.getEvent(&event);
      // Create a JSON object
      StaticJsonDocument<200> doc;
      doc["time"] = millis();
      doc["p"] = newPosition;
      doc["ax"] = int(event.acceleration.x * 1000);
      doc["ay"] = int(event.acceleration.y * 1000);
      doc["az"] = int(event.acceleration.z * 1000);

      // Serialize JSON to Serial
      serializeJson(doc, Serial);
      Serial.println();
    }
  }
}
