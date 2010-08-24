#! /usr/bin/python

#Copyright (C) 2010  Purui Wang puruiw@yahoo.com
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
#along with this program.  If not, see <http://www.gnu.org/licenses/>

import re, os, urllib
import feedparser

__author__="pwang"
__date__ ="$Aug 20, 2010 2:45:33 PM$"

app_rss_urls = ('http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/genre=6014/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/genre=6016/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topfreeapplications/sf=143441/limit=300/genre=6005/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topfreeapplications/sf=143441/limit=300/genre=6014/xml')

icon_pattern = re.compile('<img.* src=\"(.*100x100-75\.jpg)\"')

def download_icons(url, base_dir):
    """ download icons from Apple appstore """
    feed = feedparser.parse(url)
    for item in feed.entries:
        match = icon_pattern.search(item.content[0].value)
        if match:
            icon_url = match.groups()[0]    # extract icon link
            icon_url = icon_url.replace('100x100', '53x53')                        # get the smallest one
            icon_file = os.path.join(base_dir, icon_url.rpartition('/')[2])
            if not os.path.exists(icon_file):
                #print icon_url, ' => ', icon_file
                urllib.urlretrieve(icon_url, icon_file)
                yield 1
