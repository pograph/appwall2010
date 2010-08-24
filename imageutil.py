# To change this template, choose Tools | Templates
# and open the template in the editor.
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
