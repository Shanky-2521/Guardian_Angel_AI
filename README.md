# Guardian Angel - IoT Safety System

[![Arduino](https://img.shields.io/badge/Arduino-UNO%20R4%20WiFi-00979D?style=flat&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![IFTTT](https://img.shields.io/badge/IFTTT-Webhooks-FF4785?style=flat&logo=ifttt&logoColor=white)](https://ifttt.com)
[![Alexa](https://img.shields.io/badge/Amazon-Alexa-00CAFF?style=flat&logo=amazon-alexa&logoColor=white)](https://developer.amazon.com/alexa)

A complete IoT safety system that uses touch sensor input to trigger emergency alerts through Alexa voice announcements. Perfect for personal safety, elderly care, or any situation requiring quick emergency communication.

## 🛡️ Features

- **Touch-based Emergency Alerts**: Long press (3+ seconds) triggers emergency alert
- **Check-in Functionality**: Short press for routine check-ins
- **WiFi Connectivity**: Wireless communication using Arduino UNO R4 WiFi
- **Voice Announcements**: Alexa integration for home-wide alert broadcasting
- **Cloud Integration**: IFTTT webhooks for reliable alert delivery
- **Real-time Monitoring**: Python server with logging and event tracking
- **Debug Tools**: Built-in utilities for system testing and troubleshooting

## 🏗️ System Architecture

```
Touch Sensor (TTP223) → Arduino UNO R4 WiFi → WiFi Network → Python Server → IFTTT Webhook → Alexa Announcement
```

## 🔧 Hardware Requirements

- **Arduino UNO R4 WiFi** - Main microcontroller
- **TTP223 Touch Sensor** - Capacitive touch detection
- **Grove Shield** (optional) - For easy sensor connection
- **USB Cable** - For programming and power
- **WiFi Network** - 2.4GHz recommended

## 💻 Software Requirements

- **Arduino IDE** - For uploading code to Arduino
- **Python 3.7+** - For running the server
- **IFTTT Account** - For webhook integration
- **Amazon Alexa Device** - For voice announcements

## 🚀 Quick Start

### 1. Hardware Setup
1. Connect TTP223 touch sensor to Arduino pin D8
2. Power the Arduino via USB or external power supply
3. Ensure WiFi network is available

### 2. Arduino Configuration
1. Open `arduino/GuardianAngel/GuardianAngel.ino` in Arduino IDE
2. Update WiFi credentials:
   ```cpp
   const char* WIFI_SSID = "YourWiFiName";
   const char* WIFI_PASS = "YourWiFiPassword";
   const char* SERVER_HOST = "YourServerIP";
   ```
3. Upload to Arduino UNO R4 WiFi

### 3. Server Setup
1. Install Python dependencies:
   ```bash
   pip install flask requests
   ```
2. Run the server:
   ```bash
   python simple_server.py
   ```

### 4. IFTTT Integration
1. Create IFTTT account and get webhook key
2. Create applet: Webhooks → Virtual Buttons
3. Set event name: `guardian_alert`

### 5. Alexa Setup
1. Enable "Virtual Buttons" skill in Alexa app
2. Create routine: Virtual Button 01 → Voice announcement
3. Test the integration

## 📁 Project Structure

```
Guardian_Angel_AI/
├── arduino/
│   ├── GuardianAngel/
│   │   └── GuardianAngel.ino          # Main Arduino sketch
│   └── Tools/
│       ├── TouchMonitor/              # Touch sensor debugging
│       └── I2CScanner/                # I2C device scanner
├── server/
│   ├── app.py                         # Full-featured Flask server
│   ├── fixed_app.py                   # Debug version
│   └── requirements.txt               # Python dependencies
├── simple_server.py                   # Production server (recommended)
├── test_integration.py                # System testing script
├── direct_ifttt_test.py              # IFTTT webhook testing
├── ALEXA_INTEGRATION_GUIDE.md         # Detailed setup guide
└── README.md                          # This file
```

## 🎯 Usage

### Emergency Alert
1. **Long press** the touch sensor (hold for 3+ seconds)
2. Arduino sends alert to server
3. Server triggers IFTTT webhook
4. Alexa announces: *"Guardian Angel Alert!"*

### Check-in
1. **Short press** the touch sensor (less than 3 seconds)
2. System logs check-in event
3. Optional Alexa confirmation (configurable)

## 🔧 Configuration

### Arduino Settings
- **Touch Pin**: D8 (configurable)
- **Long Press Duration**: 3000ms (configurable)
- **Server Port**: 5001 (matches Python server)
- **Debounce Time**: 40ms (prevents false triggers)

### Server Settings
- **Host**: 0.0.0.0 (accepts connections from any IP)
- **Port**: 5001 (avoid conflicts with other services)
- **IFTTT Integration**: Automatic webhook sending
- **Logging**: Timestamped event logging

### IFTTT Configuration
- **Webhook Key**: Set in environment or hardcoded
- **Event Name**: `guardian_alert`
- **Target**: Virtual Buttons → Alexa routine

## 🧪 Testing

### Touch Sensor Test
```bash
# Upload TouchMonitor.ino to Arduino
# Open Serial Monitor to see raw sensor readings
```

### Server Test
```bash
python test_integration.py
```

### Direct IFTTT Test
```bash
python direct_ifttt_test.py
```

## 🛠️ Troubleshooting

### Common Issues

**Arduino won't upload:**
- Check COM port selection in Arduino IDE
- Try different USB cable
- Reset Arduino and try again

**WiFi connection fails:**
- Verify network credentials
- Ensure 2.4GHz network (5GHz not supported)
- Check signal strength

**Server not receiving requests:**
- Verify IP address in Arduino code
- Check firewall settings
- Ensure server is running on correct port

**Alexa not announcing:**
- Verify IFTTT applet is enabled
- Check Virtual Buttons skill is connected
- Test Alexa routine manually

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Arduino community for excellent documentation
- IFTTT for reliable webhook services
- Amazon Alexa for voice integration capabilities

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the `ALEXA_INTEGRATION_GUIDE.md` for detailed setup
3. Open an issue on GitHub

---

**⚠️ Safety Note**: This system is designed for convenience and basic safety applications. For critical safety situations, always have backup communication methods and consider professional monitoring services.

**🛡️ Guardian Angel - Protecting what matters most.**
