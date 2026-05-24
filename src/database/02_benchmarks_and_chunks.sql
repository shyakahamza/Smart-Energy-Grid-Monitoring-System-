 -- 1: Check Metadata & Number of Chunks Created
  SELECT hypertable_name, chunk_name, range_start, range_end FROM timescaledb_information.chunks WHERE hypertable_name IN ('energy_readings', 'energy_readings_3h', 'energy_readings_week')
  ORDER BY hypertable_name, range_start; LIMIT 5;

  -- Test 2: Compare Total Storage Disk Size
  SELECT 
      hypertable_name,
      pg_size_pretty(hypertable_size(hypertable_name::regclass)) as total_size FROM timescaledb_information.hypertables;

  -- Test 3: Compare Query Execution Speed (EXPLAIN ANALYZE)
  -- This lets you see if 3h, 1d, or 1w chunks scan faster for a 24-hour dashboard view.
  
  EXPLAIN ANALYZE 
  SELECT AVG(power), MAX(voltage) FROM energy_readings WHERE timestamp >= NOW() - INTERVAL '1 day';

  EXPLAIN ANALYZE 
  SELECT AVG(power), MAX(voltage) FROM energy_readings_3h WHERE timestamp >= NOW() - INTERVAL '1 day';

  EXPLAIN ANALYZE 
  SELECT AVG(power), MAX(voltage) FROM energy_readings_week WHERE timestamp >= NOW() - INTERVAL '1 day';
