-- 1 Create energy_readings table
CREATE TABLE energy_readings (
    meter_id VARCHAR(10) / TEXT(10),
    timestamp TIMESTAMPTZ NOT NULL,
    power DOUBLE PRECISION,
    voltage DOUBLE PRECISION,
    current DOUBLE PRECISION,
    frequency DOUBLE PRECISION,
    energy DOUBLE PRECISION
);

-- Convert it to a hypertable 
SELECT create_hypertable('energy_readings', 'timestamp', chunk_time_interval => INTERVAL '1 day');

 -- 2 Create energy_readings_3h & energy_readings_week tables from energy_readings table
CREATE TABLE energy_readings_3h (LIKE energy_readings INCLUDING ALL);
CREATE TABLE energy_readings_week (LIKE energy_readings INCLUDING ALL);

-- 3 Convert them to the respective hypertables

SELECT create_hypertable('energy_readings_3h', 'timestamp', chunk_time_interval => INTERVAL '3 hours');
SELECT create_hypertable('energy_readings_week', 'timestamp', chunk_time_interval => INTERVAL '1 week');
