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

from types import UnicodeType
from xml.sax.saxutils import escape

__known_tags = ["feature", "features", "rank", "use_for", "date", "title",
              "author", "link", "forum", "sentence", "opinions",
              "overall_rank", "percent_positive", "percent_negative",
              "total_opinions", "name", "star_rank"]

__indent_size = 2

def __print_dict(dict, indent):
    if not dict:
        return ""
    buf = ""
    lspace = " " * indent * __indent_size
    for k,v in dict.iteritems():
        if k in __known_tags:
            start_tag = "<" + k + ">"
            end_tag = "</" + k + ">"
        else:
            start_tag = "<element title=\"" + escape(str(k).strip()) + "\">"
            end_tag = "</element>"
        buf += "\n" + lspace + start_tag
        buf += to_xmls(v, indent+1)
        buf += end_tag
    return buf + "\n" + " " * (indent -1) * __indent_size

def __print_list(list, indent):
    if not list:
        return ""
    buf = ""
    lspace = " " * indent * __indent_size
    for v in list:
        buf += "\n" + lspace + "<item>"
        buf += to_xmls(v, indent+1)
        buf += "</item>"
    return buf + "\n" + " " * (indent -1) * __indent_size

def __print_scalar (value, indent):
    if value != None:
        if type(value) == UnicodeType:
            value = value.encode('utf-8')
        return escape(str(value).strip())
    else:
        return ""

def to_xmls (foo, indent = 1):
    """ Convert Python PODs to XML
    
    Takes in a Python POD (dictionary, list or scalar) and returns its XML
    representation as a string. The return value always needs to be wrapped
    in an enclosing element.
    """
    if type(foo) == type({}):
        return __print_dict(foo, indent)
    elif type(foo) == type([]) or type(foo) == type(()):
        return __print_list(foo, indent)
    else:
        return __print_scalar(foo, indent)


if __name__ == "__main__":
    dict = {"title": "Example for py2xml.to_xmls",
            "data": [
               "List item 1",
               "List item 2",
               ],
            "more data": 123,
            "finally": "We're done"
            }
    print "<?xml version=\"1.0\" ?>"
    print "<response>" + to_xmls(dict) + "</response>"
