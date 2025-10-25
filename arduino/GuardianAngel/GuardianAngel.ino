// GuardianAngel main sketch: WiFi + touch (Serial-only) + HTTP POSTs
#include <WiFiS3.h>
#include <Wire.h>

// ===== User Config =====
const char* WIFI_SSID = "Nani?";      // TODO: set (2.4 GHz WPA2 recommended)
const char* WIFI_PASS = "qwertyuiop";          // TODO: set
const char* SERVER_HOST = "10.65.219.95";      // Laptop Wi-Fi IPv4
const uint16_t SERVER_PORT = 5001;
// =======================

// Pins
const int TOUCH_PIN = 8; // D8 per Grove shield mapping

// Touch behavior
const unsigned long LONG_PRESS_MS = 3000; // 3 seconds
const unsigned long DEBOUNCE_MS = 40;
WiFiClient client;

// State
bool lastTouch = false;
unsigned long touchChangeAt = 0;
unsigned long pressStartAt = 0; // when touch goes HIGH

void setup() {
  pinMode(TOUCH_PIN, INPUT); // TTP223 outputs HIGH when touched
  Serial.begin(115200);
  delay(100);
  Serial.println("Guardian Angel starting - WiFi connecting...");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 15000) {
    delay(250);
  }

  if (WiFi.status() == WL_CONNECTED) {
    // Wait up to 10s for DHCP to provide a non-zero IP
    unsigned long dhcpStart = millis();
    while (WiFi.localIP() == IPAddress(0, 0, 0, 0) && millis() - dhcpStart < 10000) {
      delay(200);
    }
    Serial.print("WiFi connected. IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Gateway: ");
    Serial.println(WiFi.gatewayIP());
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
  } else {
    Serial.println("WiFi FAILED - check credentials");
  }
}

void loop() {
  bool touch = digitalRead(TOUCH_PIN) == HIGH;
  unsigned long now = millis();

  if (touch != lastTouch) {
    // debounce
    delay(DEBOUNCE_MS);
    touch = digitalRead(TOUCH_PIN) == HIGH;
    if (touch != lastTouch) {
      lastTouch = touch;
      touchChangeAt = now = millis();
      if (touch) {
        pressStartAt = now;
        Serial.println("Touch detected - hold for ALERT");
      } else {
        // released -> short tap
        unsigned long pressDuration = now - pressStartAt;
        if (pressDuration < LONG_PRESS_MS) {
          Serial.println("Checked In! Sending /checkin");
          postEvent("/checkin");
        }
      }
    }
  }

  if (touch && (now - touchChangeAt >= LONG_PRESS_MS)) {
    // Long press -> ALERT
    Serial.println("ALERT! Sending /alert");
    postEvent("/alert");
    // simple latch to avoid repeat until release
    while (digitalRead(TOUCH_PIN) == HIGH) {
      delay(20);
    }
    lastTouch = false;
    touchChangeAt = millis();
    Serial.println("Alert latched until release - done");
  }
}

void postEvent(const char* path) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("POST skipped - WiFi not connected");
    return;
  }
  if (!client.connect(SERVER_HOST, SERVER_PORT)) {
    Serial.println("POST connect failed");
    return;
  }
  String body = "{}";
  String req = String("POST ") + path + " HTTP/1.1\r\n" +
               "Host: " + SERVER_HOST + "\r\n" +
               "Content-Type: application/json\r\n" +
               "Content-Length: " + body.length() + "\r\n\r\n" +
               body;
  client.print(req);
  unsigned long start = millis();
  while (client.connected() && millis() - start < 500) {
    while (client.available()) client.read();
  }
  client.stop();
}
