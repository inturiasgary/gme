from datetime import datetime, date, timedelta
from dateutil import parser

def week_days(date=date.today()):
	if date.weekday() > 0:
		date= date - timedelta(days=date.weekday())
	days=list()
	for i in range(6):
		days.append(date)
		date = date + timedelta(days=1)
	days.append(date)
	return days

def week_for_date(date=date.today()):
	if date.weekday() > 0:
		date= date - timedelta(days=date.weekday())
	end_date=date+timedelta(days=6)
	return date, end_date

def parsedate(s):
	dt = parser.parse(s)
	if dt.tzinfo:
		dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
	return dt

