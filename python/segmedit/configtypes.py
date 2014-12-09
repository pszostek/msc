#!/usr/bin/env python
# encoding: utf-8

###
# Copyright 2011 University of Warsaw, Krzysztof Rusek
# 
# This file is part of SegmEdit.
#
# SegmEdit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SegmEdit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SegmEdit.  If not, see <http://www.gnu.org/licenses/>.


import collections

class ShapeStyle(object):

    def __init__(self, fillColor, strokeColor=(0, 0, 0), strokeWidth=1, dashes=None):
        self.fillColor = fillColor or (0, 0, 0, 0)
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.dashes = dashes
        self._brush = None
        self._pen = None

    @property
    def brush(self):
        pass

    @property
    def pen(self):
        pass


ZoneLabel = collections.namedtuple('ZoneLabel', 'name text style')


if __name__ == "__main__":
    print "This is a module, don't run it as a program"
