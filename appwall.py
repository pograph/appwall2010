#!/usr/bin/env python

""" 
Your own app wall. v1.1
pograph.wordpress.com
"""
import imageutil
import apputil
import pygame
from pygame.locals import *
import pymunk
from pymunk import Vec2d
import re, os, sys, copy, random
from math import *
from time import time


ICON_DIR = 'icons'
ICON_HEIGHT = 53
ICON_WIDTH = 53
ICON_MASS = 1.0
ICON_MOMENT = 100.0
GRAVITITY = -300.0

STATE_DROPPING=1
STATE_FALLING=2

class Icon(pygame.sprite.Sprite):
    def __init__(self, game, filename):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.body = pymunk.Body(ICON_MASS, ICON_MOMENT)
        a = ICON_WIDTH / 2.0
        self.shape = pymunk.Poly(self.body, [Vec2d(-a, -a), Vec2d(-a, a), Vec2d(a, a), Vec2d(a, -a)])
        self.in_space = False;
 
        # load icon, add alpha channel, and convert to pygame image
        image = imageutil.load_and_add_alpha(filename)
        image2 = pygame.image.fromstring(image.tostring(), image.size, 'RGBA')
        self.image = image2.convert_alpha()
        self.rect = self.image.get_rect()
        self.set_position(0.0, 0.0)
        self.col = 0

    def set_position(self, x, y):
        self.body.position.x = x
        self.body.position.y = y
        self.update()

    def update(self):
        if(self.in_space and self.body.position.y < -ICON_HEIGHT):
            self.game.space.remove(self.shape, self.body)
            self.in_space = False
            self.game.sprite_cols[self.col].remove(self)
            self.game.sprite_bucket.append(self)
            self.game.sprites_on_ground -= 1

        self.rect.top = int(self.game.screen_height - self.body.position.y - ICON_WIDTH / 2.0)
        self.rect.left = int(self.body.position.x - ICON_HEIGHT / 2.0)

    def render(self):
        if(self.in_space):
            self.game.screen.blit(self.image, self.rect)

    def drop(self, col):
        self.col = col
        self.set_position((col + 0.5) * ICON_WIDTH, self.game.drop_height)
        self.game.space.add(self.body, self.shape)
        self.in_space = True

    def fall(self):
        pass

class Game:
    def __init__(self):
        self.frame = 0;

        pygame.init()
        self.clock = pygame.time.Clock()
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, GRAVITITY)
        
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.grid_width = info.current_w / ICON_WIDTH + 1
        self.grid_height = info.current_h / ICON_HEIGHT + 1
        self.drop_height = self.screen_height + 1000
        
        # turn into fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

        self.font = pygame.font.Font(None, 17)

        # load icons
        self._load_files()
        self._load_sprites()
        
        self.sprite_bucket = self.sprites[:]
        self.sprites_on_ground = 0
        self.cols = []
        self.sprite_cols = []
        for i in range(self.grid_width):
            self.sprite_cols.append([])

        # create a ground
        GROUND_LEVEL = 0.0
        self.ground_body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.ground_body.position = Vec2d(0.0, GROUND_LEVEL)
        self.ground_shape = pymunk.Segment(self.ground_body, Vec2d(-10000.0, GROUND_LEVEL), Vec2d(10000.0, GROUND_LEVEL), 1.0)

        for i in range(self.grid_width + 1):
            body = pymunk.Body(pymunk.inf, pymunk.inf)
            line = pymunk.Segment(body, Vec2d(i * ICON_WIDTH, GROUND_LEVEL), Vec2d(i * ICON_WIDTH, GROUND_LEVEL + 10000.0), 0.0)
            self.space.add_static(line)
        self._init_drop()


    def run(self):
        while 1:
            self._update_state()

            for s in self.sprites:
                s.update()

            self._render()
            self.clock.tick(60)
            self.space.step(1/60.0)

            # process events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
            pygame.display.flip()
            self.frame += 1


    def _load_files(self):
        icons_needed = self.grid_width * self.grid_height
        # download icons if necessary
        if not os.path.exists(ICON_DIR):
            os.mkdir(ICON_DIR)

        files = os.listdir('icons')
        if len(files) < icons_needed:
            self._show_text('Downloading icons ...')
            cnt = 0;
            for url in apputil.app_rss_urls:
                for i in apputil.download_icons(url, 'icons'):
                    cnt += 1
                    self._show_text('Downloading icons ... %d' % cnt)
            self._show_text("")
            files = os.listdir('icons')

        if len(files) < icons_needed:
            raise SystemExit, "not enough icons"


    def _load_sprites(self):
        img_ext = ('.jpg')
        self.sprites = []
        print "Loading icons"
        icons_needed = self.grid_width * self.grid_height
        files = os.listdir('icons')
        random.shuffle(files)
        for f in files:
            if len(self.sprites) == icons_needed:
                return
            if f[-4:] in img_ext:
                try:
                    self.sprites.append(Icon(self, os.path.join('icons', f)))
                except:
                    print "ignore error on parsing ", f
                    print sys.exc_info()
        if(len(self.sprites) < icons_needed):
            raise SystemExit, "not enough icons"


    def _init_drop(self):
        self.cols = range(self.grid_width)[:]
        self.space.add_static(self.ground_shape)
        self.state = STATE_DROPPING

    def _init_fall(self):
        self.cols = range(self.grid_width)[:]
        self.space.remove_static(self.ground_shape)
        self.state = STATE_FALLING

    def _update_state(self):
        if(self.state == STATE_DROPPING):
            if(len(self.sprite_bucket) == 0):
                self._init_fall()
                return

            # drop a icon randomly
            if(random.randint(0, 100) % 10 == 0):
                icon = self.sprite_bucket.pop()
                col = random.choice(self.cols)
                self.sprite_cols[col].append(icon)
                if(len(self.sprite_cols[col]) == self.grid_height):
                    self.cols.remove(col)
                self.sprites_on_ground += 1
                icon.drop(col)

        elif(self.state == STATE_FALLING):
            if(self.sprites_on_ground == 0):
                self._init_drop()
                return
        
    def _render(self):
        self.screen.fill((0, 0, 0))
        for s in self.sprites:
            s.render()

    def _show_text(self, msg):
        text = self.font.render(msg, True, (255, 255, 255), (0, 0, 0))
        rect = text.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.centery = self.screen.get_rect().centery
        self.screen.blit(text, rect)
        pygame.display.update()

if __name__ == '__main__':
    print "Welcome to your own App Wall."
    g = Game()
    g.run()
