// TouchMonitor: prints raw D8 readings and edge timings
// Board: Arduino UNO R4 WiFi

const int TOUCH_PIN = 8; // Grove D8
const unsigned long SAMPLE_MS = 50; // print every 50ms

bool lastState = false;
unsigned long lastPrint = 0;
unsigned long pressStart = 0;

void setup() {
  pinMode(TOUCH_PIN, INPUT); // TTP223 usually outputs HIGH on touch
  Serial.begin(115200);
  delay(100);
  Serial.println("TouchMonitor starting...");
  Serial.println("Expected: 0 when idle, 1 (HIGH) when touched.");
}

void loop() {
  bool s = digitalRead(TOUCH_PIN) == HIGH;
  unsigned long now = millis();

  if (s != lastState) {
    // edge detected
    if (s) {
      pressStart = now;
      Serial.print("EDGE: TOUCH DOWN at ");
      Serial.print(now);
      Serial.println(" ms");
    } else {
      unsigned long dur = now - pressStart;
      Serial.print("EDGE: TOUCH UP at ");
      Serial.print(now);
      Serial.print(" ms, duration=");
      Serial.print(dur);
      Serial.println(" ms");
    }
    lastState = s;
  }

  if (now - lastPrint >= SAMPLE_MS) {
    Serial.print("RAW: ");
    Serial.println(s ? 1 : 0);
    lastPrint = now;
  }
}
