import random
import math
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

TOTAL_METERS = 1000
BATCH_SIZE = 100000

random.seed(42)
METER_IDS = [str(random.randint(1000000000, 9999999999)) for _ in range(TOTAL_METERS)]

def calculate_realistic_power(dt_obj):
    hour = dt_obj.hour + (dt_obj.minute / 60.0)
    base_load = 0.2
    morning_peak = 1.5 * math.exp(-0.5 * ((hour - 8.0) / 1.0) ** 2)
    evening_peak = 2.5 * math.exp(-0.5 * ((hour - 19.5) / 1.5) ** 2)
    noise = random.uniform(-0.05, 0.05)
    return max(0.05, round(base_load + morning_peak + evening_peak + noise, 3))

def load_history():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 4 weeks of data (28 days back from today)
    now = datetime.now()
    current_time = now - timedelta(days=28)
    
    meter_energy = {m_id: random.uniform(50.0, 200.0) for m_id in METER_IDS}
    data_buffer = []
    inserted_count = 0
    
    print("Generating and loading 8.4 million history rows...")
    
    while current_time <= now:
        for m_id in METER_IDS:
            power = calculate_realistic_power(current_time)
            voltage = round(random.uniform(225.0, 245.0), 1)
            current = round((power * 1000) / voltage, 2)
            frequency = round(random.uniform(49.8, 50.2), 2)
            meter_energy[m_id] += power * (5 / 60)
            
            data_buffer.append((
                m_id, current_time.strftime("%Y-%m-%d %H:%M:%S"),
                power, voltage, current, frequency, round(meter_energy[m_id], 4)
            ))
            
            if len(data_buffer) >= BATCH_SIZE:
                execute_values(cursor, "INSERT INTO energy_readings VALUES %s", data_buffer)
                conn.commit()
                inserted_count += len(data_buffer)
                print(f"Loaded {inserted_count} rows...")
                data_buffer.clear()
                
        current_time += timedelta(minutes=5)
        
    if data_buffer:
        execute_values(cursor, "INSERT INTO energy_readings VALUES %s", data_buffer)
        conn.commit()
        inserted_count += len(data_buffer)
        
    print(f"Success! Final Total: {inserted_count} rows loaded.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_history()
