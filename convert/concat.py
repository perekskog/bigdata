#!/usr/bin/env python3
""" Concatenate JSON files

Usage:

    concat input1 input2 output

Args:
    input1  First inputfile
    input2  Second inputfile
    output Outputfile
"""

import sys
import json


def datetime_parser(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, AttributeError, TypeError):
            pass
    return json_dict


def main(filein1, filein2, fileout):
    items1 = json.load(open(filein1, 'r', encoding="utf-8"), object_hook=datetime_parser)
    items2 = json.load(open(filein2, 'r', encoding="utf-8"), object_hook=datetime_parser)
    item = item1 + items2
    open(fileout, 'wb').write(json.dumps(items, sort_keys=False, indent=4, ensure_ascii=False)
                              .encode('utf8'))



if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("{}".format(__doc__))
