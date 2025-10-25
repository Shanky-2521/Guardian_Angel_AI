/*
 * Guardian Angel AI - Arduino R4 WiFi Code
 * 
 * This code connects to WiFi, reads a touch sensor, and sends
 * check-in/alert events to the Flask backend.
 * 
 * Hardware:
 * - Arduino Uno R4 WiFi
 * - Touch Sensor connected to Digital Pin 2
 * 
 * Setup:
 * 1. Install WiFiS3 library (built-in for R4)
 * 2. Install ArduinoHttpClient library
 * 3. Update WiFi credentials and server IP below
 */

#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

// WiFi credentials
const char* ssid = "Nani?";
const char* password = "qwertyuiop";

// Backend server info (your laptop's IP address)
const char* serverIP = "10.65.219.51";  // Change to your laptop's IP
const int serverPort = 5000;

// Touch sensor pin
const int touchPin = 2;

// Timing variables
unsigned long touchStartTime = 0;
bool isTouching = false;
bool alertSent = false;
unsigned long lastCheckinTime = 0;
const unsigned long CHECKIN_COOLDOWN = 5000;  // 5 seconds between check-ins
const unsigned long ALERT_THRESHOLD = 3000;   // 3 seconds for alert

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverIP, serverPort);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  pinMode(touchPin, INPUT);
  
  Serial.println("🛡️  Guardian Angel AI Starting...");
  
  // Connect to WiFi
  connectWiFi();
}

void loop() {
  int touchState = digitalRead(touchPin);
  unsigned long currentTime = millis();
  
  // Touch detected
  if (touchState == HIGH) {
    if (!isTouching) {
      // Touch just started
      isTouching = true;
      touchStartTime = currentTime;
      alertSent = false;
      Serial.println("Touch detected...");
    }
    
    unsigned long touchDuration = currentTime - touchStartTime;
    
    // Check if held long enough for alert (3 seconds)
    if (touchDuration >= ALERT_THRESHOLD && !alertSent) {
      Serial.println("⚠️  ALERT THRESHOLD REACHED!");
      sendAlert();
      alertSent = true;
    }
  } 
  // Touch released
  else {
    if (isTouching) {
      unsigned long touchDuration = currentTime - touchStartTime;
      
      // If released before alert threshold, it's a check-in
      if (touchDuration < ALERT_THRESHOLD && !alertSent) {
        // Check cooldown to prevent spam
        if (currentTime - lastCheckinTime > CHECKIN_COOLDOWN) {
          Serial.println("✓ Check-in detected");
          sendCheckin();
          lastCheckinTime = currentTime;
        }
      }
      
      isTouching = false;
      alertSent = false;
    }
  }
  
  delay(50);  // Small delay for stability
}

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Connecting to server: ");
    Serial.print(serverIP);
    Serial.print(":");
    Serial.println(serverPort);
  } else {
    Serial.println("\n✗ WiFi Connection Failed!");
  }
}

void sendCheckin() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected!");
    return;
  }
  
  Serial.println("Sending check-in to server...");
  
  client.post("/api/checkin");
  
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();
  
  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
  
  if (statusCode == 200) {
    Serial.println("✓ Check-in sent successfully!");
  } else {
    Serial.println("✗ Check-in failed!");
  }
}

void sendAlert() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected!");
    return;
  }
  
  Serial.println("🚨 SENDING ALERT TO SERVER...");
  
  String jsonBody = "{\"description\": \"Emergency alert - Touch sensor held for 3 seconds\"}";
  
  client.post("/api/alert", "application/json", jsonBody);
  
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();
  
  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
  
  if (statusCode == 200) {
    Serial.println("✓ ALERT SENT SUCCESSFULLY!");
  } else {
    Serial.println("✗ ALERT FAILED!");
  }
}

/*
 * SETUP INSTRUCTIONS:
 * 
 * 1. Hardware Setup:
 *    - Connect touch sensor VCC to 5V
 *    - Connect touch sensor GND to GND
 *    - Connect touch sensor SIG to Digital Pin 2
 * 
 * 2. Get Your Laptop IP:
 *    Mac/Linux: Open Terminal and run: ifconfig | grep "inet "
 *    Windows: Open CMD and run: ipconfig
 *    Look for something like 192.168.1.100 (your local network IP)
 * 
 * 3. Update Code:
 *    - Change ssid to your WiFi network name
 *    - Change password to your WiFi password
 *    - Change serverIP to your laptop's IP address from step 2
 * 
 * 4. Upload to Arduino R4 WiFi
 * 
 * 5. Make sure Flask backend is running on your laptop!
 * 
 * 6. Open Serial Monitor (115200 baud) to see debug output
 * 
 * TESTING:
 * - Quick tap: Sends check-in (green event on dashboard)
 * - Hold 3+ seconds: Sends alert (red event + Echo Dot announcement)
 */
