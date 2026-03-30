from yolobit import *
from aiot_lcd1602 import LCD1602
from aiot_dht20 import DHT20
import time
import network_module
import coreiot_module
from mqtt import mqtt # Import để gọi check_msg
import fan_module

# Khởi tạo phần cứng
lcd = LCD1602()
dht = DHT20()
light_sensor = pin2

lcd.clear()
print("Khoi dong YOLO Home...")

# Kết nối mạng
network_module.connect_wifi(lcd)
network_module.sync_time(lcd)
coreiot_module.setup_adafruit(lcd) 

last_send_time = 0
send_interval = 5 # Gửi lên Cloud mỗi 5 giây 

while True:
    try:
        mqtt.check_msg()
        temp = dht.dht20_temperature()
        humi = dht.dht20_humidity()
        light_percent = int((light_sensor.read_analog() / 1023) * 100)
        
        t = time.localtime(time.time() + 7 * 3600)
        line1 = "{:>4.1f}*C {:>3d}% {:>3d}%".format(temp, int(humi), light_percent)
        line2 = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}".format(t[2], t[1], t[0], t[3], t[4])
        lcd.move_to(0, 0); lcd.putstr(line1)
        lcd.move_to(0, 1); lcd.putstr(line2)

        current_time = time.time()
        if current_time - last_send_time >= 5: # Đổi thành 10 giây
            coreiot_module.publish_sensor_data(temp, humi, light_percent)
            last_send_time = current_time 
            print("--- Da cap nhat Cloud ---")

    except Exception as e:
        print("Loi he thong, dang thu tiep tuc:", e)
    
    time.sleep(0.1)