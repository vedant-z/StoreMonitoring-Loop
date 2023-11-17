from store_monitor.models import StoreStatus, BusinessHours, StoreReport, StoreTimezone
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import random
import string
import json
from pytz import timezone

def generate_report():
    # Get all store_ids
    store_ids = StoreStatus.objects.values_list('store_id', flat=True).distinct()

    aggregated_report_data = []

    for random_store_id in store_ids:
        # Get the latest timestamp from the StoreStatus model for the selected store
        latest_timestamp = StoreStatus.objects.filter(store_id=random_store_id).latest('timestamp_utc').timestamp_utc

        # Get the timezone information for the selected store
        try:
            store_timezone = StoreTimezone.objects.get(store_id=random_store_id)
            tz = timezone(store_timezone.timezone_str)
        except StoreTimezone.DoesNotExist:
            # If timezone data is missing, assume it is America/Chicago
            tz = timezone('America/Chicago')

        # Convert timestamps to the store's local timezone
        latest_timestamp_local = latest_timestamp.astimezone(tz)

        # Define the time intervals for the report
        last_hour_start_time = latest_timestamp_local - timedelta(hours=1)
        last_day_start_time = latest_timestamp_local - timedelta(days=1)
        last_week_start_time = latest_timestamp_local - timedelta(weeks=1)
        report_end_time = latest_timestamp_local

        # Extract data for the specific store
        store_status_data = StoreStatus.objects.filter(store_id=random_store_id, timestamp_utc__range=(last_week_start_time, report_end_time))
        business_hours_data = BusinessHours.objects.filter(store_id=random_store_id)

        # Initialize arrays to store statuses and timestamps
        timestamps = []
        statuses = []

        # Extract observed statuses and timestamps
        for status in store_status_data:
            timestamps.append(status.timestamp_utc)
            statuses.append(status.status)

        # Convert timestamps to numeric values
        numeric_timestamps = mdates.date2num(timestamps)

        # Convert statuses to numeric values
        numeric_statuses = np.where(np.array(statuses) == 'active', 1, 0)

        # Convert numeric_statuses to native Python list of integers
        numeric_statuses = numeric_statuses.tolist()

        # Interpolate numeric statuses for the entire business hours interval
        business_hours_interval = pd.date_range(last_week_start_time, report_end_time, freq='1H')
        numeric_business_hours_interval = mdates.date2num(business_hours_interval)
        interpolated_statuses = np.interp(numeric_business_hours_interval, numeric_timestamps, numeric_statuses, left=0, right=0)

        # Calculate uptime and downtime for the entire interval
        total_business_hours = len(business_hours_interval)
        uptime = np.sum(interpolated_statuses == 1)
        downtime = total_business_hours - uptime

        # Calculate uptime and downtime for the last hour
        last_hour_statuses = interpolated_statuses[-1:]  # Last 1 hour
        last_hour_uptime = np.sum(last_hour_statuses == 1)
        last_hour_downtime = 1 - last_hour_uptime  # Total hours - uptime

        # Calculate uptime and downtime for the last day
        last_day_statuses = interpolated_statuses[-24:]  # Last 24 hours
        last_day_uptime = np.sum(last_day_statuses == 1)
        last_day_downtime = 24 - last_day_uptime  # Total hours - uptime

        # Calculate uptime and downtime for the last week
        last_week_uptime = np.sum(interpolated_statuses == 1)
        last_week_downtime = total_business_hours - last_week_uptime

        # Append the data to the aggregated_report_data list
        report_data = {
            'store_id': random_store_id,
            'uptime_last_hour': int(last_hour_uptime * 60),  # Convert hours to minutes
            'uptime_last_day': int(last_day_uptime),
            'uptime_last_week': int(last_week_uptime),
            'downtime_last_hour': int(last_hour_downtime * 60),  # Convert hours to minutes
            'downtime_last_day': int(last_day_downtime),
            'downtime_last_week': int(last_week_downtime),
        }

        aggregated_report_data.append(report_data)

    # Store the aggregated report data in the database
    report_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    StoreReport.objects.create(report_id=report_id, data=json.dumps(aggregated_report_data))

    return report_id  # Return the single report_id