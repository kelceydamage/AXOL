from datetime import datetime, timedelta
now = datetime.utcnow()
rounded = now - timedelta(minutes=now.minute % 5 + 5,
                          seconds=now.second,
                          microseconds=now.microsecond)
print rounded
now = str(datetime.utcnow())
print str(now[8:15])


