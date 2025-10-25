# Guardian Angel - Alexa Integration Guide

## Method 1: IFTTT + Webhooks (Recommended - Easy Setup)

### Step 1: Setup IFTTT Account
1. Go to [ifttt.com](https://ifttt.com) and create an account
2. Go to [ifttt.com/maker_webhooks](https://ifttt.com/maker_webhooks)
3. Click "Connect" to enable Webhooks service
4. Go to [ifttt.com/maker_webhooks/settings](https://ifttt.com/maker_webhooks/settings)
5. Copy your webhook key (looks like: `dBZlTzLbFYAHHWOo_XXXXX`)

### Step 2: Create IFTTT Applets

#### For Emergency Alerts:
1. Go to [ifttt.com/create](https://ifttt.com/create)
2. **IF This**: Choose "Webhooks" → "Receive a web request"
   - Event Name: `guardian_alert`
3. **Then That**: Choose "Amazon Alexa" → "Say a specific phrase"
   - What do you want Alexa to say: `Emergency alert from Guardian Angel! {{Value1}} at {{Value2}}`
   - OR choose "Send Alexa notification" for a less intrusive notification

#### For Check-ins (Optional):
1. Create another applet
2. **IF This**: Choose "Webhooks" → "Receive a web request"
   - Event Name: `guardian_checkin`
3. **Then That**: Choose "Amazon Alexa" → "Say a specific phrase"
   - What do you want Alexa to say: `Guardian Angel check-in received. All is well.`

### Step 3: Configure Environment Variables

Set these environment variables on your server:

```bash
# Required for alerts
IFTTT_WEBHOOK_KEY=your_webhook_key_here
IFTTT_EVENT_NAME=guardian_alert

# Optional for check-ins
IFTTT_CHECKIN_EVENT=guardian_checkin
IFTTT_ENABLE_CHECKIN=1
```

### Step 4: Test the Integration

1. Start your Python server
2. Test the alert endpoint:
   ```bash
   curl -X POST http://your-server-ip:5000/alert
   ```
3. Alexa should announce the alert!

---

## Method 2: Home Assistant + Alexa (Advanced)

### Requirements:
- Home Assistant installation
- Alexa integration in Home Assistant

### Step 1: Install Home Assistant
1. Install Home Assistant on your network
2. Add the Alexa integration

### Step 2: Modify Guardian Angel Server
Add Home Assistant webhook integration:

```python
# Add to your server environment variables
HOMEASSISTANT_URL=http://your-ha-ip:8123
HOMEASSISTANT_TOKEN=your_long_lived_access_token
```

### Step 3: Create Home Assistant Automations
Create automations that trigger Alexa announcements when webhooks are received.

---

## Method 3: AWS Lambda + Alexa Skills Kit (Most Advanced)

### Overview:
Create a custom Alexa skill that receives notifications from your Guardian Angel.

### Requirements:
- AWS Account
- Alexa Developer Account
- More complex setup

### Steps:
1. Create AWS Lambda function to receive Guardian Angel webhooks
2. Create custom Alexa skill
3. Link skill to Lambda function
4. Configure proactive events API

---

## Troubleshooting

### IFTTT Method Issues:
- **Webhook not triggering**: Check your webhook key and event names
- **Alexa not responding**: Ensure your Alexa device is connected and IFTTT Alexa service is linked
- **Delayed responses**: IFTTT can have 1-15 minute delays (normal)

### Testing Commands:
```bash
# Test alert
curl -X POST http://10.65.219.95:5000/alert

# Test check-in
curl -X POST http://10.65.219.95:5000/checkin
```

### Environment Variables Setup (Windows):
```cmd
set IFTTT_WEBHOOK_KEY=your_key_here
set IFTTT_EVENT_NAME=guardian_alert
python server/app.py
```

### Environment Variables Setup (PowerShell):
```powershell
$env:IFTTT_WEBHOOK_KEY="your_key_here"
$env:IFTTT_EVENT_NAME="guardian_alert"
python server/app.py
```

---

## Recommended Setup

**Start with Method 1 (IFTTT)** - it's the easiest and most reliable for your use case.

The IFTTT method will:
- ✅ Work immediately with existing Alexa devices
- ✅ No complex configuration
- ✅ Free for basic usage
- ✅ Reliable webhook delivery
- ✅ Can trigger multiple actions (notifications, announcements, smart home devices)

Once you have IFTTT working, you can explore the other methods if you need more advanced features.
