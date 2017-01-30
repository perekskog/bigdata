""" Batch convert csv files exported from TimePOlice app.
"""
import sys
import json
from datetime import datetime
from timepolice_csv2json import fetch_items

sheets = [
    {'name': "21 dec - 27 dec-Tabell 1.csv", 'basedate': "15-12-21", 'columns':
     [0, 2, 4, 6, 8, 10, 12]},
    {'name': "30 dec - 4 jan-Tabell 1.csv", 'basedate': "15-12-30", 'columns': [0, 2, 4, 6, 8, 10]}
]

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, ...):
        return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable'
                        % (type(obj), repr(obj)))

def main(basedirectory, json_store):
    f = open(json_store, 'wb')
    sessions = list()
    for sheet in sheets:
        for column in sheet['columns']:
            items = fetch_items(basedirectory+"/"+sheet['name'], "utf-8", ';',
                                datetime.strptime(sheet['basedate'], "%y-%m-%d"), column)
            for session in items:
                sessions.append(session)
    f.write(json.dumps(sessions, sort_keys=True, indent=4, default=date_handler,
                       ensure_ascii=False).encode('utf8'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
