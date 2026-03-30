# adafruit_module.py
import time
from mqtt import mqtt
import config
import fan_module
#import rgb_module

def setup_adafruit(lcd):
    print("Connecting to Adafruit IO...")
    try:
        mqtt.connect_ww_or_tt(
            config.AIO_BROKER, 
            config.AIO_PORT, 
            config.AIO_USERNAME, # User
            config.AIO_KEY,      # Password (Key)
            config.AIO_USERNAME  # Client ID
        )

        mqtt.on_receive_message(config.FEED_FAN, fan_module.fan_callback)
        #mqtt.on_receive_message(config.FEED_RGB, rgb_module.led_callback)
        lcd.clear()
        lcd.putstr("Adafruit OK!")
        print("Subscribed to Fan and RGB feeds")
    except Exception as e:
        print("Error:", e)

def publish_sensor_data(temp, humi, light):
    try:
        mqtt.publish(config.FEED_TEMP, str(temp))
        mqtt.publish(config.FEED_HUMI, str(humi))
        mqtt.publish(config.FEED_LIGHT, str(light))
        #mqtt.publish(config.FEED_FAN, str(fan_speed))
        print("Sent to Adafruit!")
    except Exception as e:
        print("Loi gui MQTT, dang thu ket noi lai...")
        try:
            # Gọi lại hàm setup để kết nối lại nếu bị rớt mạng
            mqtt.connect_ww_or_tt(
                config.AIO_BROKER, 
                config.AIO_PORT, 
                config.AIO_USERNAME, 
                config.AIO_KEY, 
                config.AIO_USERNAME
            )
        except:
            pass