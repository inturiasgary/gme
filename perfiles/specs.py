#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from imagekit.specs import ImageSpec
from imagekit import processors

# define the thumnail processor
class ResizeThumb(processors.Resize):
    width = 100
    height = 75
    crop = True

class ResizeDisplay(processors.Resize):
    width = 600

class ResizeBig(processors.Resize):
    width = 800

# define your spec
class Thumbnail(ImageSpec):
    pre_cache = True
    processors = [ResizeThumb,]

class Display(ImageSpec):
    processors = [ResizeDisplay,]

class Big(ImageSpec):
    processors = [ResizeBig,]
