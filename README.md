YOLO Home - Smart Monitoring System
1. Overview
YOLO Home is an IoT-based smart home project designed to monitor environmental conditions and provide a user-friendly control interface. The system collects data from various sensors and transmits it to a cloud dashboard for real-time visualization.

3. Tech Stack
- Hardware: Yolo:bit (ESP32-based), DHT20 (Temperature & Humidity), Light Sensor, PIR Motion Sensor, LCD Display.
- Firmware: MicroPython.
- Communication Protocol: MQTT (via Adafruit IO).
- Frontend: HTML, CSS, and JavaScript.
- Data Format: JSON (used for structured data packaging and exchange).

3. Key Features
- Real-time Data Acquisition: Reads temperature, humidity, and light levels every few seconds.
- Motion Detection: Uses a PIR sensor to detect movement and trigger alerts.
- Cloud Integration: Synchronizes all sensor data with Adafruit IO using the MQTT protocol for remote access.
- Interactive Dashboard: A web interface built with JavaScript to visualize live data feeds and manage device states.
- Local Feedback: Displays current system status and sensor readings on a physical LCD.

4. System Architecture
- Sensing Layer: Yolo:bit gathers raw data from connected sensors.
- Processing Layer: The MicroPython firmware processes the data and formats it into JSON strings.
- Transport Layer: Data is published to specific MQTT topics on Adafruit IO.
- Application Layer: The web dashboard subscribes to these topics. JavaScript logic handles asynchronous data updates and refreshes the UI without reloading the page.

5. Installation & Setup
- Flash the MicroPython firmware to your Yolo:bit.
- Configure your WiFi credentials and Adafruit IO API keys in the source code.
- Connect the sensors to the designated GPIO pins.
- Open the index.html file in your browser to view the dashboard.
