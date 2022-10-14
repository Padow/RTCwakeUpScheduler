#!/usr/bin/python3
import datetime,time,yaml,math,os,sys
from yaml.loader import SafeLoader
from pytz import timezone

week_days = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
now = datetime.datetime.now(timezone('Europe/Paris'))
config_file = os.path.abspath(os.path.dirname(sys.argv[0]))+os.sep+"rtc_wake_up_config.yaml"

with open(config_file, "r") as stream:
	try:
		data = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

def write_wake_alarm(next_boot_date):
	with open('/sys/class/rtc/rtc0/wakealarm', 'w') as f:
		f.write(next_boot_date)

def set_new_date_time(hour, add_days):
	hm = hour.split('h')
	return (now + datetime.timedelta(days = add_days)).replace(hour=int(hm[0]), minute=int(hm[1]), second=00)

def get_week_day(days):
	intWeekDay = days - ((math.floor((days) / 7)) * 7)
	return week_days[intWeekDay]

def find_boot_date(week_day, add_days):
	hours = data.get(get_week_day(week_day + add_days))
	for hour in hours or []:
		nb = set_new_date_time(hour, add_days)
		if nb > now:
			return nb

def get_next_boot_date(current_date):
	week_day = current_date.weekday()
	next_boot_date = None
	add_days = 0
	while (next_boot_date is None) and (add_days < 8):
		next_boot_date = find_boot_date(week_day, add_days)
		add_days += 1
	return str(time.mktime(next_boot_date.timetuple())).split(".")[0] if next_boot_date is not None else str(0)

# clean wakealarm
write_wake_alarm(str(0))
# set new boot date 
write_wake_alarm(get_next_boot_date(now))
