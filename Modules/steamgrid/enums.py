"""
The MIT License (MIT)
Copyright (c) 2015-present Rapptz
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from enum import Enum


__all__ = [
    'PlatformType',
    'StyleType',
    'MimeType',
    'ImageType',
]

class PlatformType(Enum):
    Steam = 'steam'
    Origin =  'origin'
    Egs = 'egs'
    Bnet = 'bnet'
    Uplay = 'uplay'
    Flashpoint = 'flashpoint'
    Eshop = 'eshop'

    def __str__(self) -> str:
        return self.name

class StyleType(Enum):
    Alternate = 'alternate'
    Blurred = 'blurred'
    White_logo = 'white_logo'
    Material = 'material'
    No_logo = 'no_logo'

    def __str__(self) -> str:
        return self.name

class MimeType(Enum):
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    WEBP = 'image/webp'

    def __str__(self) -> str:
        return self.name

class ImageType(Enum):
    Static = 'static '
    Animated = 'animated'

    def __str__(self) -> str:
        return self.name

class AssetType(Enum):
    Grid = 'grids'
    Hero = 'heroes'
    Logo = 'logoes'
    Icon = 'icons'

    def __str__(self) -> str:
        return self.name