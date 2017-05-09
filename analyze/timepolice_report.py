#!/usr/bin/env python3
""" Extract information from timepolice data

Usage:

    timepolice_report store report firstdata lastdate distribution

Args:
    store   JSON file with timepolice data
    report
        timesheet   Summary of sessions of type "Kostnad"
    firstdata   First date to include, yy-mm-dd
    lastdate    Last date to include, yy-mm-dd
    distribution    JSON file defining how tasks should be distributed

"""
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

def session_summary(session, distributions):
    summary = dict()

    for taskentry in session['taskentries']:
        name = taskentry['taskname']
        distribution = get_distribution(distributions, taskentry['start'])
        # print(distribution)
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
    return summary


def timesheet(store, first_date, last_date, distribution):
    first = datetime.strptime(first_date, "%y-%m-%d").date().toordinal()
    last = datetime.strptime(last_date, "%y-%m-%d").date().toordinal()
    subset_kostnad = [s for s in store if session_between_dates(s, "Kostnad", first, last)]

    tasknames = set()
    for session in subset_kostnad:
        summary = session_summary(session, distribution)
        print(session['date_created'].date())
        for task in summary:
            print(task, round(summary[task].seconds/3600, 2))
        totals = [s for s in summary.values()]
        total = functools.reduce(lambda x, y: x+y, totals)
        print(round(total.seconds/3600, 2))
        print()


def main(store, report, first_date, last_date, distribution):
    storeitems = json.load(open(store, 'r', encoding="utf-8"), object_hook=datetime_parser)
    if report == "timesheet":
        distributionitems = json.load(open(distribution, 'r', encoding="utf-8"),
                                      object_hook=datetime_parser)
        timesheet(storeitems, first_date, last_date, distributionitems)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("{}".format(__doc__))
