#!/usr/bin/python

# Copyright (c) WisdomTap Solutions (I) Pvt Ltd. All rights reserved.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, codecs, simplejson

max_rank = 1000 #rank value for #1 item in a list
step = 10 #difference in rank values of consecutive items

def main(args):
    if len(args) < 3:
        print "Usage: " + args[0] + " <reference_list> <list> [<list>... ]"
    
    reflist = build_list(args[1]) # Only interested in position stats
    lists = dict([(x, build_list(x)) for x in args[2:]])
    
    for lname, ldata in lists.iteritems():
        dump_stats(lname, ldata, reflist)
    
def build_list(fname):
    f = codecs.open(fname, 'r', 'utf-8')
    pos = 0
    p_stats = {}
    lines = [x.strip() for x in f.readlines()]
    for line in lines:
        rank = max_rank - pos*step
        p_stats[line.lower()] = [pos, rank]
        pos += 1
    
    return (lines, p_stats)

def dump_stats(lname, ldata, reflist):
    print "Stats for %s:\n" % lname
    (refnames, reflist) = reflist
    (items, p_stats) = ldata
    deviation = 0
    for item in items:
        if item.lower() in reflist:
            pos_gain = "%+03d" % (reflist[item.lower()][0] - p_stats[item.lower()][0])
            deviation += abs(p_stats[item.lower()][1] - reflist[item.lower()][1])
        else:
            pos_gain = "+++"
        print "%s: %s" % (item, pos_gain)
    missing = set(reflist.keys()) - set(p_stats.keys())
    
    if len(missing):
        for item in missing:
            deviation += reflist[item][1]
            print "%s: %s" % (refnames[reflist[item][0]], "---")
    
    print "Deviation: %d" % deviation
    print "==========================\n"
    
if __name__ == '__main__':
    main(sys.argv)
