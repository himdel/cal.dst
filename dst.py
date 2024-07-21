#!/usr/bin/env python3
# coding=utf-8

from ics import Calendar, Event
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY, SU

def calculate_dst_dates(start_year, num_years):
  dst_dates = []
  for year in range(start_year, start_year + num_years):
    # EU DST changes (last Sunday of March and October)
    eu_dst_start = list(rrule(MONTHLY, count=1, bymonth=3, byweekday=SU(-1), dtstart=datetime(year, 3, 1)))[0]
    eu_dst_end = list(rrule(MONTHLY, count=1, bymonth=10, byweekday=SU(-1), dtstart=datetime(year, 10, 1)))[0]

    # US DST changes (second Sunday of March and first Sunday of November)
    us_dst_start = list(rrule(MONTHLY, count=1, bymonth=3, byweekday=SU(2), dtstart=datetime(year, 3, 1)))[0]
    us_dst_end = list(rrule(MONTHLY, count=1, bymonth=11, byweekday=SU(1), dtstart=datetime(year, 11, 1)))[0]

    dst_dates.append((year, eu_dst_start, eu_dst_end, us_dst_start, us_dst_end))

  return dst_dates

def create_dst_event(title, start_date, end_date):
  event = Event()
  event.name = title
  event.begin = start_date
  event.end = end_date
  return event

def generate_icalendar(dst_dates):
  calendar = Calendar()

  for i, (year, eu_dst_start, eu_dst_end, us_dst_start, us_dst_end) in enumerate(dst_dates, start=1):
    calendar.events.add(create_dst_event(f'EU DST Start {year}', eu_dst_start, eu_dst_start + timedelta(hours=1)))
    calendar.events.add(create_dst_event(f'EU DST End {year}', eu_dst_end - timedelta(hours=1), eu_dst_end))
    calendar.events.add(create_dst_event(f'US DST Start {year}', us_dst_start, us_dst_start + timedelta(hours=1)))
    calendar.events.add(create_dst_event(f'US DST End {year}', us_dst_end - timedelta(hours=1), us_dst_end))

  return calendar

# Define the start year and the number of years to precompute
start_year = datetime.today().year
num_years = 5

# Calculate DST change dates
dst_dates = calculate_dst_dates(start_year, num_years)

# Generate iCalendar
calendar = generate_icalendar(dst_dates)

# Save the calendar to a file
with open('/dev/stdout', 'w') as f:
  f.writelines(calendar)
