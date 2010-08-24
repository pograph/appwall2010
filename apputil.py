#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
import re
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
                print icon_url, ' => ', icon_file
                urllib.urlretrieve(icon_url, icon_file)

def download_all_icons():
    print "Downloading icons..."
    for url in app_rss_urls:
        download_icons(url)

if __name__ == "__main__":
    print "Hello World";
