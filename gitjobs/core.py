# -*- coding: utf-8 -*-

"""
Example of usage: #TODO

"""

try:
    import simplejson as json
except ImportError:
    import json

import urllib2
import urllib
import time
import datetime

__all__ = ['Position', 'Positions', 'ApiRequestError']

GITJOBS_BASE = "http://jobs.github.com/"
POSITIONS = "%spositions/" % GITJOBS_BASE
SEARCH = "%spositions.json" % GITJOBS_BASE


class InvalidRequestArguments(Exception):
    pass

class ApiRequestError(Exception):
    pass

class Position(object):

    def __init__(self, position_id=None, markdown=False, ext=".json"):
        self.position_id = position_id
        self.markdown = markdown
        self.ext = ext
        self._id = self.position_id+self.ext

    def __repr__(self):
        return '<Position %s>' % self.position_id

    def __getattribute__(self, value):
        attr_names = ('id', 'company', 'location', 'created_at',
            'company_url', 'title', 'company_logo', 'type', 'how_to_apply',
            'description')

        if value in attr_names:
            if not hasattr(self, '_data'):
                self._data = json.loads(self._get_json())
            for item in attr_names:
                setattr(self, item, unicode(self._data[item]))
        return object.__getattribute__(self, value)

    def _prepare_request(self):
        url = POSITIONS+self._id
        if self.markdown:
            url = url + "?markdown=true"
        return url

    def _get_json(self):
        try:
            data = urllib2.urlopen(self._prepare_request())
            if data.code != 200:
                raise ApiRequestError
        except urllib2.URLError:
            raise ApiRequestError
        else:
            return data.read()

    @property
    def created(self):
        "Set custom property for date objects to be valid python date"
        time_format = "%a %b %d %H:%M:%S %Z %Y"
        t = time.strptime(self.created_at, time_format)
        return datetime.datetime(
            year=t.tm_year,
            month=t.tm_mon,
            day=t.tm_mday,
            hour=t.tm_hour,
            minute=t.tm_min,
            second=t.tm_sec
        )


class Positions(object):

    def __init__(self, description=None, location=None,
                 lat=None, long=None, full_time=True):
        self.description = description
        self.location = location
        self.lat = lat
        self.long = long
        self.full_time = full_time

    def __len__(self):
        return self.count

    def __repr__(self):
        return "<Positions %s>" % self.description

    def _prepare_request(self):
        func = lambda x: x if x else ""
        args = {
            'description': func(self.description),
            'location': func(self.location),
            'full_time': func(self.full_time)
        }

        if any([self.lat, self.long]) and self.location:
            raise InvalidRequestArguments

        if self.lat and self.long:
            args['lat'] = self.lat
            args['long'] = self.long
        url = urllib.urlencode(args)
        return SEARCH + "?" + url

    def _get_json(self):
        try:
            data = urllib2.urlopen(self._prepare_request())
            if data.code != 200:
                raise ApiRequestError
        except urllib2.URLError:
            raise ApiRequestError
        else:
            return data.read()

    @property
    def items(self):
        if not hasattr(self, 'positions'):
            positions = list()
            for item in json.loads(self._get_json()):
                position = Position(position_id=item['id'])
                setattr(position, '_data', item)
                positions.append(position)
            setattr(self, 'positions', positions)
        return self.positions

    @property
    def count(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield  item

    def next(self):
        #TODO, fix this method to avoid changing object
        items = self.items
        try:
            return items.pop()
        except IndexError:
            raise StopIteration
