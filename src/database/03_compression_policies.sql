 -- 1. ENABLE COMPRESSION STATEMENTS
-- Enable compression on the 1 Hour hypertable
ALTER TABLE energy_readings SET (timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC'); 

-- Enable compression on the 3 hour hypertable
ALTER TABLER energy_readings_3h SET(timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC');

-- Enable compression on the 1 week hypertable
ALTER TABLE energy_readings_week SET(timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC');

 -- 2. AUTOMATED COMPRESSION POLICIES
-- Automatically compress chunks older than 7 days on the main hypertable
SELECT add_compression_policy('energy_readings', INTERVAL '7 days');

-- For the 3-hour hypertable, compress aggressively after 1 day
SELECT add_compression_policy('energy_readings_3h', INTERVAL '1 day');

-- For the 1-week hypertable, compress after 14 days
SELECT add_compression_policy('energy_readings_week', INTERVAL '14 days');
