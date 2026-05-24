import json
import psycopg2
from paho.mqtt import client as mqtt_client

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",       # Your database name
    "user": "postgres",         # Your database user
    "password": "postgres", # Your actual database password
    "host": "localhost",
    "port": 5432
}

def insert_to_db(cursor, data):
    """Stores data fields exactly as required by the specification"""
    query = """
    INSERT INTO energy_readings (meter_id, timestamp, power, voltage, current, frequency, energy)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (
        data['meter_id'], 
        data['timestamp'], 
        data['power'], 
        data['voltage'], 
        data['current'], 
        data['frequency'], 
        data['energy']
    ))

def on_message(client, userdata, msg):
    conn = userdata['db_conn']
    cursor = conn.cursor()
    try:
        # Step 2 requirement: Parse incoming JSON payload
        payload = json.loads(msg.payload.decode())
        
        insert_to_db(cursor, payload)
        conn.commit()
        print(f"Successfully stored message from meter: {payload['meter_id']}")
    except Exception as e:
        conn.rollback()
        print(f"Error processing payload: {e}")
    finally:
        cursor.close()

def main():
    db_conn = psycopg2.connect(**DB_CONFIG)
    
    # Initialize paho-mqtt client
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, userdata={'db_conn': db_conn})
    client.on_message = on_message
    
    client.connect("localhost", 1883)
    client.subscribe("energy/meters/#") # Step 1 requirement
    
    print("Subscriber bridge running. Awaiting messages...")
    client.loop_forever()

if __name__ == "__main__":
    main()
