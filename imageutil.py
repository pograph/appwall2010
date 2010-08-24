
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

import Image

__author__="pwang"
__date__ ="$Aug 20, 2010 3:11:33 PM$"

# alpha channel
alpha_chan = Image.open('template.png').split()

def load_and_add_alpha(filename):
    """ load image and add alpha channel """
    rgb_chan = Image.open(filename).split()
    if len(rgb_chan) >= 3:
        image = Image.merge('RGBA', (rgb_chan[0], rgb_chan[1], rgb_chan[2], alpha_chan[0]))
    else:
        image = Image.merge('RGBA', (rgb_chan[0], rgb_chan[0], rgb_chan[0], alpha_chan[0]))
    return image

if __name__ == "__main__":
    print "Hello World"
