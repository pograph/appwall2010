#!/bin/bash
rm -rf dist build
python setup-osx.py py2app
cp build/bdist.macosx-10.3-fat/python2.5-standalone/app/collect/pymunk/libchipmunk.dylib dist/appwall.app/Contents/Frameworks/

