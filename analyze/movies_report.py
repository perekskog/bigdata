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
    movies = dict()
    for movie in store:
        m = {"media-location": movie["media-location"],
             "media-format": movie["media-format"],
             "media-type": movie["media-type"]}
        movies[movie["title"]] = m
    return movies


def main(store, report):
    items = json.load(open(store, 'r', encoding="utf-8"), object_hook=datetime_parser)
    movies = list()
    if report == "movielist":
        movies = movielist(items)

    titles = movies.keys()
    sorted_titles = sorted(titles)
    for title in sorted_titles:
        movie_data = movies[title]
        print("{}\t{}\t{}/{}".format(movie_data["media-location"], title, movie_data["media-type"], movie_data["media-format"]))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("{}".format(__doc__))
