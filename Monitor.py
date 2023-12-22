import time
import requests
import wmi

def get_cpu_info():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        cpu_temp = None
        cpu_power = None
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                cpu_temp = sensor.Value
            elif sensor.SensorType == 'Power' and 'CPU' in sensor.Name:
                cpu_power = sensor.Value
        return cpu_temp, cpu_power
    except Exception as e:
        print(f"Error getting CPU information: {e}")
    return "CPU temperature not available", "CPU power usage not available"

def get_gpu_info():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        gpu_temp = None
        gpu_power = None
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'GPU' in sensor.Name:
                gpu_temp = sensor.Value
            elif sensor.SensorType == 'Power' and 'GPU' in sensor.Name:
                gpu_power = sensor.Value
        return gpu_temp, gpu_power
    except Exception as e:
        print(f"Error getting GPU information: {e}")
    return "GPU temperature not available", "GPU power usage not available"

def get_motherboard_power():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == 'Power' and 'Motherboard' in sensor.Name:
                return sensor.Value
    except Exception as e:
        print(f"Error getting motherboard power: {e}")
    return "Motherboard power not available"

def send_to_discord(cpu_temp, gpu_temp, cpu_power, gpu_power, max_cpu_temp, max_gpu_temp, max_cpu_power, max_gpu_power):
    webhook_url = "UR_WEBHOOK"
    avg_temp = 40
    high_temp = 80

    if cpu_temp > high_temp or gpu_temp > high_temp:
        color = 0xFF0000  # Red for high temperature
    elif cpu_temp > avg_temp or gpu_temp > avg_temp:
        color = 0xFFFF00  # Yellow for average temperature
    else:
        color = 0x00FF00  # Green for normal temperature

    embed = {
        "title": "System Temperature and Power Usage",
        "color": color,
        "fields": [
            {"name": "CPU Temperature", "value": f"{cpu_temp:.1f}°C", "inline": True},
            {"name": "GPU Temperature", "value": f"{gpu_temp:.1f}°C", "inline": True},
            {"name": "CPU Power Usage", "value": f"{cpu_power:.1f} W", "inline": True},
            {"name": "GPU Power Usage", "value": f"{gpu_power:.1f} W", "inline": True},
            {"name": "Total Power Usage", "value": f"{cpu_power + gpu_power:.1f} W", "inline": True},
            {"name": "Max CPU Temp", "value": f"{max_cpu_temp:.1f}°C", "inline": True},
            {"name": "Max GPU Temp", "value": f"{max_gpu_temp:.1f}°C", "inline": True},
            {"name": "Max CPU Power", "value": f"{max_cpu_power:.1f} W", "inline": True},
            {"name": "Max GPU Power", "value": f"{max_gpu_power:.1f} W", "inline": True},
        ],
        "footer": {"text": "System Monitoring"}
    }

    data = {
        "embeds": [embed]
    }

    try:
        result = requests.post(webhook_url, json=data)
        if result.status_code != 204:
            print(f"Failed to send message to Discord: {result.status_code}")
    except Exception as e:
        print(f"Error sending message to Discord: {e}")

max_cpu_temp = 0
max_gpu_temp = 0
max_cpu_power = 0
max_gpu_power = 0

while True:
    cpu_temp, cpu_power = get_cpu_info()
    gpu_temp, gpu_power = get_gpu_info()

    max_cpu_temp = max(max_cpu_temp, cpu_temp)
    max_gpu_temp = max(max_gpu_temp, gpu_temp)
    max_cpu_power = max(max_cpu_power, cpu_power)
    max_gpu_power = max(max_gpu_power, gpu_power)

    send_to_discord(cpu_temp, gpu_temp, cpu_power, gpu_power, max_cpu_temp, max_gpu_temp, max_cpu_power, max_gpu_power)

    time.sleep(5) # How long until next send in seconds
