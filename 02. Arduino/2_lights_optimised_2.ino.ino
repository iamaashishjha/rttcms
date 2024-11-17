const int redPins[] = { 12, 2 };
const int yellowPins[] = { 10, 3 };
const int greenPins[] = { 8, 4 };
const int trigPins[] = { 13, 6 };  // Ultrasonic trigger pins
const int echoPins[] = { 11, 5 };  // Ultrasonic echo pins

unsigned long lastReadTime = 0;
const long interval = 1000;  // Time between sensor readings (ms)

void setup() {
  for (int i = 0; i < 2; i++) {
    pinMode(redPins[i], OUTPUT);
    pinMode(yellowPins[i], OUTPUT);
    pinMode(greenPins[i], OUTPUT);
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
  }

  Serial.begin(9600);
  Serial.println("Setup complete, waiting for commands...");
}

long measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  return (duration > 0) ? (duration * 0.034) / 2 : -1;  // Return distance or -1 if no valid pulse
}

void controlLEDs(int index, const String& color, int distance) {
  digitalWrite(redPins[index], LOW);
  digitalWrite(yellowPins[index], LOW);
  digitalWrite(greenPins[index], LOW);

  // MESSAGE TO PYTHON
  Serial.print("LED_");
  Serial.print(index);
  Serial.print("=");
  Serial.print(color);
  Serial.print(":");
  Serial.print("SENSOR_");
  Serial.print(index);
  Serial.print("=");
  Serial.println(distance);

  if (color == "green") {
    digitalWrite(greenPins[index], HIGH);
  } else if (color == "yellow") {
    digitalWrite(yellowPins[index], HIGH);
  } else if (color == "red") {
    digitalWrite(redPins[index], HIGH);
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastReadTime >= interval) {
    lastReadTime = currentMillis;

    for (int i = 0; i < 2; i++) {
      long distance = measureDistance(trigPins[i], echoPins[i]);
      if (distance >= 0) {
        if (distance < 5) {
          controlLEDs(i, "green", distance);
        } else if (distance < 10) {
          controlLEDs(i, "yellow", distance);
        } else {
          controlLEDs(i, "red", distance);
        }
      } else {
        Serial.print("SENSOR_");
        Serial.print(i);
        Serial.println(": No valid distance");
      }
    }
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("green") || command.startsWith("yellow") || command.startsWith("red")) {
      int index = command.substring(command.length() - 1).toInt();
      controlLEDs(index, command.substring(0, command.length() - 1), 100);
    }
  }
}
