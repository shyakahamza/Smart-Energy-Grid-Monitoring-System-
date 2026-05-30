# Smart Grid Analytics Engine (TimescaleDB & Grafana)

## Setup & Installation
1. **Database Setup**: Install TimescaleDB locally, connect to your PostgreSQL instance, and execute the SQL scripts found in `src/database/` in sequential order.
2. **Data Generation**: Install dependencies and run the historical ingestion pipeline:
   ```bash
   pip install -r requirements.txt
   python src/pipeline_subscriber.py
   python src/data_simulation/data_generator/py
   python src/data_simulation/bulk_history_loader.py
   
   
   ```
3. **Dashboard Access**: Install Grafana natively on your OS. Access via `http://localhost:3000`, add your local PostgreSQL database as a data source, and import the JSON template from the `grafana/` directory.


## Summary to getting started 
1. Run the SQL scripts in `src/database/` sequentially on your TimescaleDB instance.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the generator: `python src/data_simulation/bulk_history_loader.py`
