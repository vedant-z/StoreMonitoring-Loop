# Store Monitoring System

## Overview

This Django-based Store Monitoring System tracks the status of stores and generates reports detailing uptime and downtime for specific time intervals. The system includes two main components: the data collection module and the reporting module.

## Features

- **Data Collection:** Ingests store status data and business hours from CSV files into the database.
- **Reporting:** Generates reports for each store, including uptime and downtime calculations.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/store-monitoring.git
    cd store-monitoring
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations:

    ```bash
    python manage.py migrate
    ```

4. Load data into the database:

    ```bash
    python manage.py loaddata
    ```

## Uptime and Downtime calculation 

**The interpolation logic, implemented using NumPy's np.interp function, helps in estimating the status of the store for every hour within the business hours interval. This ensures that even if there are only a few observations available, the entire business hours interval is filled with estimated statuses based on the available data.**

Here's a brief overview of how the logic achieves this:

### Interpolation:

The observed status data is interpolated to cover the entire business hours interval, filling the gaps between the available observations.
The np.interp function is used for this interpolation, and it takes care of estimating the statuses for the entire interval based on the available observations.

### Numeric Representation:

The status values ('active' or 'inactive') are numerically represented (e.g., 1 for 'active' and 0 for 'inactive') to facilitate numerical operations.

### Calculation of Uptime and Downtime:

Uptime and downtime are then calculated based on the interpolated numeric statuses, ensuring that the entire business hours interval is considered.

## API Endpoints

1. `/trigger_report`:
    - Endpoint to trigger report generation.
    - Output: `report_id` (random string).

2. `/get_report/<report_id>`:
    - Endpoint to get the status of the report or the complete CSV report.
    - Input: `report_id`.
    - Output:
        - If report generation is not complete, return "Running."
        - If report generation is complete, return "Complete" along with the CSV file.

## Usage

1. Trigger Report Generation:

    ```bash
    curl -X POST http://localhost:8000/trigger_report/
    ```

    Output: `{"report_id": "random_string"}`

2. Get Report Status or CSV:

    ```bash
    curl http://localhost:8000/get_report/random_string/
    ```

    Output:
    - If running: `{"status": "Running"}`
    - If complete: `{"status": "Complete", "report": {...}}`
