#!/usr/bin/env python3
""" Extract information from movie data

Usage:

    movies_report store report

Args:
    store   JSON file with movie data
    report  
        movielist   Alphabetical list of movies

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


def movielist(store):
    movies = list()
    for movie in store:
        # Add default values
        if not "production-year" in movie:
            movie["production-year"] = -1
        if not "comment" in movie:
            movie["comment"] = ""
        m = {"media-title": movie["title"],
             "media-location": movie["media-location"],
             "media-type": movie["media-type"],
             "media-format": movie["media-format"],
             "media-audio": movie["audio"],
             "media-subtitle": movie["subtitle"],
             "media-comment": movie["comment"],
             "media-production-year": movie["production-year"]}
        # if movie["title"] in movies:
        #     print("{} already exists, skipping this one.".format(movie["title"]))
        #     continue
        movies.append(m)
    return movies


def main(store, report):
    items = json.load(open(store, 'r', encoding="utf-8"), object_hook=datetime_parser)
    movies = list()
    if report == "movielist":
        movies = movielist(items)

    movies.sort(key=lambda movie: movie["media-title"])
    for movie in movies:
        if movie["media-production-year"] == -1:
            print("{}\t{}\t{}/{}".
                format(movie["media-location"],
                        movie["media-title"],
                        movie["media-type"],
                        movie["media-format"]))
        else:
            print("{}\t{} ({})\t{}/{}".
                format(movie["media-location"],
                        movie["media-title"],
                        movie["media-production-year"],
                        movie["media-type"],
                        movie["media-format"]))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("{}".format(__doc__))
