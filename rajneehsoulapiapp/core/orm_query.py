from django.db import connection

from rajneehsoulapiapp.address.models import Address


query = """
SELECT a.*, s.dateTime AS schedule_time, s.id AS sid
FROM rajneehsoulapiapp_address AS a
INNER JOIN rajneehsoulapiapp_emailidregistration AS e ON a.user_id = e.id
INNER JOIN rajneehsoulapiapp_scheduleitemlist AS s ON s.user_id = e.id
WHERE s.isWeatherNotifyEnabled = TRUE;
"""
results = list(Address.objects.raw(query))
