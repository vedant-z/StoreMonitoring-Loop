from django.core.management.base import BaseCommand
import pandas as pd
from store_monitor.models import StoreStatus, BusinessHours, StoreTimezone
import dateutil.parser
from datetime import timedelta
import numpy as np

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        file_path_status = 'C:\\Users\\vedant\\Downloads\\store status.csv'
        file_path_business_hours = 'https://drive.google.com/uc?id=1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg'
        file_path_timezone = 'https://drive.google.com/uc?id=101P9quxHoMZMZCVWQ5o-shonk2lgK1-o'

        # Read the CSV file for store_status_data
        store_status_data = pd.read_csv(file_path_status)

        # Parse the timestamp_utc column with dateutil.parser
        store_status_data['timestamp_utc'] = store_status_data['timestamp_utc'].apply(lambda x: dateutil.parser.parse(x))

        # Prepare a list of StoreStatus objects
        store_status_objects = [
            StoreStatus(
                store_id=row['store_id'],
                timestamp_utc=row['timestamp_utc'],
                status=row['status']
            )
            for index, row in store_status_data.iterrows()
        ]

        # Bulk insert the data into the database
        StoreStatus.objects.bulk_create(store_status_objects)

        # Read business_hours_data
        business_hours_data = pd.read_csv(file_path_business_hours)

        # Handle missing data for business hours (assuming 24/7 if missing)
        business_hours_data = business_hours_data.fillna({'start_time_local': '00:00', 'end_time_local': '23:59'})

        for index, row in business_hours_data.iterrows():
            BusinessHours.objects.create(
                store_id=row['store_id'],
                day=row['day'],
                start_time_local=row['start_time_local'],
                end_time_local=row['end_time_local']
            )

        # Read store_timezone_data
        store_timezone_data = pd.read_csv(file_path_timezone)

        # Handle missing data for timezone (assuming 'America/Chicago' if missing)
        store_timezone_data['timezone_str'] = store_timezone_data['timezone_str'].fillna('America/Chicago')

        for index, row in store_timezone_data.iterrows():
            StoreTimezone.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str']
            )