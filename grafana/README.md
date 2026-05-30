This project is a Grafana-based smart grid monitoring and performance analysis system using TimescaleDB.
It visualizes real-time and historical energy data while also evaluating database optimization techniques like continuous aggregates and compression.

The repository contains two main dashboards:
1. Smart Grid Analytics Dashboard
   
- Shows real-time and historical energy consumption data
- Includes meter readings, weekly trends, daily comparisons, and regional usage
- Helps monitor energy demand, detect spikes, and analyze consumption patterns

2. Performance Metrics Dashboard

- Evaluates TimescaleDB performance improvements
- Compares raw queries vs continuous aggregates
- Measures storage efficiency before and after compression

The project demonstrates how Grafana and TimescaleDB can be used together to monitor smart grid energy usage and optimize database performance through advanced time-series techniques.

Importing Dashboards
---------------------
1. Open Grafana
2. Navigate to Dashboards -> Import
3. Upload one of the JSON files in Grafana folder
4. Select the appropriate data source
5. Import
