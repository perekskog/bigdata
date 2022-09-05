#!/usr/bin/env python3

import argparse
import sys
import json
import functools
from datetime import datetime, date, time, timedelta


def datetime_parser(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, AttributeError, TypeError):
            pass
    return json_dict


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, ...):
        return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


def session_between_dates(session, projectname, startdate, enddate):
    if session['projectname'] == projectname and session['date_created'].date().toordinal() >= startdate and session['date_created'].date().toordinal() <= enddate:
        return True
    else:
        return False


def add_task(summary, name, time):
    try:
        summary[name] += time
    except KeyError:
        summary[name] = time

def get_distribution(distributions, start):
    dist = []
    for d in reversed(distributions):
        if d['start_date'] < start:
            dist = d['distribution']
            break
    return dist

def append_session_summary(summary, session, distributions):
    for taskentry in session['taskentries']:
        name = taskentry['taskname']
        distribution = get_distribution(distributions, taskentry['start'])
        totaltime = taskentry['stop']-taskentry['start']
        found = False
        for origin in distribution:
            if origin['origin_task'] == name:
                for new in origin['distribute_as']:
                    add_task(summary, new['new_task'], totaltime * new['new_amount'])
                found = True
                break
        if found == False:
            add_task(summary, name, totaltime)

def print_summary(summary_text, last_date_included, summary):
    totals = [s for s in summary.values()]

    for task in summary:
        print(task, round(summary[task].total_seconds()/3600, 2))

    if(len(totals) > 0):
        totalseconds = functools.reduce(lambda x, y: x+y, totals).total_seconds()
        (_,week,_) = last_date_included.isocalendar()
        print("{} {} (week {}) ===> {}".format(summary_text, last_date_included, week, round(totalseconds/3600, 2)))
        print()
        return totalseconds

    return 0

def period_done(old_session_created, current_session_created, period):
    if(old_session_created==()):
        return False
    if(period=='daily'):
        return True
    elif(period=='weekly'):
        (_,current_week,_) = current_session_created.isocalendar()
        (_,old_week,_) = old_session_created.isocalendar()
        if(current_week != old_week):
            return True
        else:
            return False
    elif(period=='monthly'):
        if(current_session_created.month != old_session_created.month):
            return True
        else:
            return False


def timesheet(store, first_date, last_date, distribution, project, period):
    first = datetime.strptime(first_date, "%y-%m-%d").date().toordinal()
    last = datetime.strptime(last_date, "%y-%m-%d").date().toordinal()
    subset_kostnad = [s for s in store if session_between_dates(s, project, first, last)]
    summary = dict()
    old_session_created = ()
    total_seconds = 0
    for session in subset_kostnad:
        if(period_done(old_session_created, session['date_created'], period)):
            period_seconds = print_summary("Last date included", old_session_created, summary)
            total_seconds = total_seconds + period_seconds
            summary = dict()
        append_session_summary(summary, session, distribution)
        old_session_created = session['date_created']
    period_seconds = print_summary("Last date included", subset_kostnad[-1]['date_created'], summary)
    total_seconds = total_seconds + period_seconds
    print("Total: {}".format(round(total_seconds/3600, 2)))
    print()
        




default_startdate = '19-06-01'
default_enddate = '19-12-31'

# Varför göra detta?
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract information from timepolice data')
    parser.add_argument("datastore", help="JSON file with timepolice data")
    parser.add_argument("--startdate", help="First date to include, yy-mm-dd", default=default_startdate, action='store')
    parser.add_argument("--enddate", help="Last date to include, yy-mm-dd", default=default_enddate, action='store')
    parser.add_argument("--distribution", help="JSON file defining how tasks should be distributed", action='store')
    parser.add_argument("--report", help="", action='store', default='timesheet')
    parser.add_argument("--project", help="Name of project to analyze", action='store', default='Kostnad')
    parser.add_argument("--period", help="Periodicity for sums", action='store', choices=['daily','weekly','monthly'], default='weekly')
    args = parser.parse_args()
    datastore = args.datastore
    report = args.report
    startdate = args.startdate
    enddate = args.enddate
    project = args.project
    period = args.period

    storeitems = json.load(open(datastore, 'r', encoding="utf-8"), object_hook=datetime_parser)

    if report == "timesheet":
        distributionitems = []
        if(args.distribution):
            distribution = args.distribution
            distributionitems = json.load(open(distribution, 'r', encoding="utf-8"),
                                      object_hook=datetime_parser)
        timesheet(storeitems, startdate, enddate, distributionitems, project, period)

