import json
import time
import random
import math
from datetime import datetime, timedelta
from paho.mqtt import client as mqtt_client

BROKER = 'localhost'
PORT = 1883
TOTAL_METERS = 1000

# Step 2 requirement: Generate 1000 distinct 10-digit meter IDs
random.seed(101)
METER_IDS = [str(random.randint(1000000000, 9999999999)) for _ in range(TOTAL_METERS)]

def calculate_realistic_power(dt_obj):
    """Step 2 requirement: Higher usage in morning/evening, lower at night"""
    hour = dt_obj.hour + (dt_obj.minute / 60.0)
    base_load = 0.2  # background power usage
    morning_peak = 1.5 * math.exp(-0.5 * ((hour - 8.0) / 1.0) ** 2)   # Peak around 8 AM
    evening_peak = 2.5 * math.exp(-0.5 * ((hour - 19.5) / 1.5) ** 2) # Peak around 7:30 PM
    noise = random.uniform(-0.05, 0.05)
    return max(0.05, round(base_load + morning_peak + evening_peak + noise, 3))

def run_test_generation():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT)
    client.loop_start()

    # Track historical accumulated energy per meter
    meter_energy_tracker = {m_id: 0.0 for m_id in METER_IDS}

    # Step 2 requirement: Generate data for exactly 1 hour (12 cycles of 5-minute increments)
    start_time = datetime.now() - timedelta(hours=1)
    
    print("Starting 1-hour data generation test for 1,000 meters...")
    
    for cycle in range(12):
        timestamp_snapshot = start_time + timedelta(minutes=5 * cycle)
        print(f"Simulating time slice: {timestamp_snapshot.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for meter_id in METER_IDS:
            power = calculate_realistic_power(timestamp_snapshot)
            voltage = round(random.uniform(225.0, 245.0), 1)
            current = round((power * 1000) / voltage, 2)
            frequency = round(random.uniform(49.8, 50.2), 2)
            
            # 5 minutes accumulation = power * (5 / 60) hours
            meter_energy_tracker[meter_id] += power * (5 / 60)
            
            # Step 2 requirement: Message format must be JSON with required fields
            payload = {
                "meter_id": meter_id,
                "timestamp": timestamp_snapshot.strftime("%Y-%m-%d %H:%M:%S"),
                "power": power,
                "voltage": voltage,
                "current": current,
                "frequency": frequency,
                "energy": round(meter_energy_tracker[meter_id], 4)
            }
            
            # Step 2 requirement: Publish to topic energy/meters/{meter_id}
            topic = f"energy/meters/{meter_id}"
            client.publish(topic, json.dumps(payload), qos=0)
            
        # Give EMQX broker a tiny fraction of a second to breathe between 1,000-message bursts
        time.sleep(0.1)

    client.loop_stop()
    print("1-Hour test simulation finished publishing!")

if __name__ == "__main__":
    run_test_generation()
