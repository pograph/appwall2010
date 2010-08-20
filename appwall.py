#!/usr/bin/env python

""" 
Your own app wall. v1.1
pograph.wordpress.com
"""
import pygame
from pygame.locals import *
import Image

import feedparser
import re, os, sys, urllib, copy, random
from math import *
from time import time

app_rss_urls = ('http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/genre=6014/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/toppaidapplications/sf=143441/limit=300/genre=6016/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topfreeapplications/sf=143441/limit=300/genre=6005/xml',
                'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topfreeapplications/sf=143441/limit=300/genre=6014/xml')
ICON_DIR = 'icons'
ICON_HEIGHT = 53
ICON_WIDTH = 53

icon_pattern = re.compile('<img.* src=\"(.*100x100-75\.jpg)\"')
grid_width = 0
grid_height = 0

def id_to_xy(id):
    return id % grid_width, id / grid_width

def xy_to_id(x, y):
    return x + y * grid_width

def download_icons(url):
    """ download icons from Apple appstore """
    feed = feedparser.parse(url)
    for item in feed.entries:
        match = icon_pattern.search(item.content[0].value)
        if match:
            icon_url = match.groups()[0]    # extract icon link
            icon_url = icon_url.replace('100x100', '53x53')                        # get the smallest one
            icon_file = os.path.join('icons', icon_url.rpartition('/')[2])
            if not os.path.exists(icon_file):
                print icon_url, ' => ', icon_file
                urllib.urlretrieve(icon_url, icon_file)

class Icon(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)

        # load image and add alpha channel
        rgb_chan = Image.open(filename).split()
        alpha_chan = Image.open('template.png').split()
        if len(rgb_chan) >= 3:
            image = Image.merge('RGBA', (rgb_chan[0], rgb_chan[1], rgb_chan[2], alpha_chan[0]))
        else:
            image = Image.merge('RGBA', (rgb_chan[0], rgb_chan[0], rgb_chan[0], alpha_chan[0]))

        # convert to pygame image
        image2 = pygame.image.fromstring(image.tostring(), image.size, 'RGBA')
        self.image = image2.convert_alpha()
        self.rect = self.image.get_rect()
        self.orig_rect = copy.deepcopy(self.rect)
        self.z = 0

    def update_pos(self):
        """ fake 3D effect """
        self.rect.left = self.orig_rect.left + self.z * -0.866 * 50
        self.rect.top = self.orig_rect.top + self.z * -0.5 * 50

def load_files(files):
    img_ext = ('.jpg')
    sprites = []
    print "Loading icons"
    for f in files:
        if len(sprites) == grid_width * grid_height:
            return sprites
        if f[-4:] in img_ext:
            try:
                sprites.append(Icon(os.path.join('icons', f)))
            except:
                print "ignore error on parsing ", f
                print sys.exc_info()
                pass
    return sprites

def assign_sprites(sprites):
    for i in range(len(sprites)):
        sprites[i].id = i;
        sprites[i].rect.top = (i / grid_width) * ICON_HEIGHT
        sprites[i].rect.left = (i % grid_width) * ICON_WIDTH
        sprites[i].orig_rect = copy.deepcopy(sprites[i].rect)
        sprites[i].x, sprites[i].y = id_to_xy(i)

def main():
    global grid_width, grid_height
    print "Welcome to your own App Wall."

    pygame.init()

    # init grid
    info = pygame.display.Info()
    grid_width = info.current_w / ICON_WIDTH + 1
    grid_height = info.current_h / ICON_HEIGHT + 1
    icons_needed = grid_width * grid_height

    # init
    clock = pygame.time.Clock()
    rand = random.Random()
    start_time = time()
    last_change_time = start_time

    # download icons if necessary
    if not os.path.exists(ICON_DIR):
        os.mkdir(ICON_DIR)

    files = os.listdir('icons')
    if len(files) < icons_needed:
        print "Downloading icons..."
        for url in app_rss_urls:
            download_icons(url)
        files = os.listdir('icons')

    if len(files) < icons_needed:
        raise SystemExit, "not enough icons"

    # turn into fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    # create a black image, use it to simulate lighting effects
    #black_image = pygame.Surface((ICON_WIDTH, ICON_HEIGHT))
    #black_image = black_image.convert()
    #black_image.fill((0, 0, 0))

    # load icons
    sprites = load_files(files)
    if len(sprites) < icons_needed:
        raise SystemExit, "not enough icons"
        
    random.shuffle(sprites)
    assign_sprites(sprites)

    while 1:
        clock.tick(60)
        tnow = time()
        for s in sprites:
            s.z = 0

        if tnow - last_change_time > 3600:    # re arrange icons every 1 hr
            del waves[:]
            random.shuffle(sprites)
            assign_sprites(sprites)
            last_change_time = tnow

        for s in sprites:
            s.update_pos()

        # draw sprites

        screen.fill((0, 0, 0))
        for s in sprites:
            screen.blit(s.image, s.rect)
            # draw black image above sprite to simulate lighting
            #black_image.set_alpha(z_to_alpha(s.z))
            #screen.blit(black_image, s.rect)

        # process events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        pygame.display.flip()

if __name__ == '__main__':
    main()
