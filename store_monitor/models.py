from django.db import models

class StoreStatus(models.Model):
    store_id = models.IntegerField()
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

class BusinessHours(models.Model):
    store_id = models.IntegerField()
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreTimezone(models.Model):
    store_id = models.IntegerField()
    timezone_str = models.CharField(max_length=50)

class StoreReport(models.Model):
    report_id = models.CharField(max_length=10, unique=True)
    data = models.JSONField(default=list)  # Set a default value (empty list) for 'data'

    def to_dict(self):
        if self.data:
            return {
                'store_id': self.data['store_id'],
                'uptime_last_hour': self.data['uptime_last_hour'],
                'uptime_last_day': self.data['uptime_last_day'],
                'uptime_last_week': self.data['uptime_last_week'],
                'downtime_last_hour': self.data['downtime_last_hour'],
                'downtime_last_day': self.data['downtime_last_day'],
                'downtime_last_week': self.data['downtime_last_week'],
            }
        else:
            return {}