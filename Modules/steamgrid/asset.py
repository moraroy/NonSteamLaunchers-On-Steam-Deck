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

from typing import Tuple, Iterator, Any

from .http import HTTPClient
from .author import Author
from .enums import AssetType

__all__ = (
    'Grid',
    'Hero',
    'Logo',
    'Icon',
)

class Asset:
    """Base class for all assets.

    Depending on the way this object was created, some of the attributes can
    have a value of ``None``.

    .. container:: operations
        .. describe:: x == y
            Checks if two asset are the same.
        .. describe:: x != y
            Checks if two asset are not the same.
        .. describe:: iter(x)
            Returns an iterator of ``(field, value)`` pairs. This allows this class
            to be used as an iterable in list/dict/etc constructions.
        .. describe:: str(x)
            Returns a string representation of the asset.


    Attributes
    -----------
    id: :class:`str`
        The asset's ID.
    author: :class:`Author`
        The author of the asset.
    score: :class:`int`
        The asset's score.
    width: :class:`int`
        The asset's width.
    height: :class:`int`
        The asset's width.
    style: :class:`str`
        The style of the asset.
    notes: Optional[:class:`str`]
        Notes about the asset.
    mime: :class:`str`
        The MIME type of the asset.
    language: :class:`str`
        The language of the asset.
    url: :class:`str`
        The URL of the asset.
    thumbnail: :class:`str`
        The URL of the asset's thumbnail.
    type: :class:`AssetType`
        The type of the asset.
    """

    __slots__: Tuple[str, ...] = (
        '_payload',
        '_http',
        'id',
        'score',
        'width',
        'height',
        'style',
        '_nsfw',
        '_humor',
        'notes',
        'mime',
        'language',
        'url',
        'thumbnail',
        '_lock',
        '_epilepsy',
        'type',
        'author'
    )

    def __init__(self, payload: dict, type: AssetType,  http: HTTPClient) -> None:
        self._payload = payload
        self._http = http
        self._from_data(payload)
        self.type = type

    def _from_data(self, asset: dict):
        self.id = asset.get('id')
        self.author: Author = Author(asset['author'])
        self.score = asset.get('score')
        self.width = asset.get('width')
        self.height = asset.get('height')
        self.style = asset.get('style')
        self._nsfw = asset.get('nsfw')
        self._humor = asset.get('humor')
        self.notes = asset.get('notes', None)
        self.mime = asset.get('mime')
        self.language = asset.get('language')
        self.url = asset.get('url')
        self.thumbnail = asset.get('thumb')
        self._lock = asset.get('lock')
        self._epilepsy = asset.get('epilepsy')
        self.upvotes = asset.get('upvotes')
        self.downvotes = asset.get('downvotes')

    def __str__(self) -> str:
        return self.url

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other) -> bool:
        return self.id != other.id

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for attr in self.__slots__:
            if attr[0] != '_':
                value = getattr(self, attr, None)
                if value is not None:
                    yield (attr, value)

    def to_json(self) -> dict:
        return self._payload

    def is_lock(self) -> bool:
        """:class:`bool`: Returns whether the asset is locked."""
        return self.lock

    def is_humor(self) -> bool:
        """:class:`bool`: Returns whether the asset is a humor asset."""
        return self.humor

    def is_nsfw(self) -> bool:
        """:class:`bool`: Returns whether the asset is NSFW."""
        return self.nsfw

    def is_epilepsy(self) -> bool:
        """:class:`bool`: Returns whether the asset is epilepsy-inducing."""
        return self.is_epilepsy


class Grid(Asset):
    def __init__(self, payload: dict, http: HTTPClient) -> None:
        super().__init__(
            payload, 
            AssetType.Grid,
            http
        )
    
    def __repr__(self) -> str:
        return f'<Grid id={self.id} height={self.height} width={self.width} author={self.author.name}>'

    def delete(self) -> None:
        """Delete the grid."""
        self._http.delete_grid([self.id])

class Hero(Asset):
    def __init__(self, payload: dict, http: HTTPClient) -> None:
        super().__init__(
            payload, 
            AssetType.Hero,
            http
        )
    
    def __repr__(self) -> str:
        return f'<Hero id={self.id} height={self.height} width={self.width} author={self.author.name}>'
    
    def delete(self) -> None:
        """Delete the hero."""
        self._http.delete_hero([self.id])

class Logo(Asset):
    def __init__(self, payload: dict, http: HTTPClient) -> None:
        super().__init__(
            payload, 
            AssetType.Logo,
            http
        )
    
    def __repr__(self) -> str:
        return f'<Logo id={self.id} height={self.height} width={self.width} author={self.author.name}>'
    
    def delete(self) -> None:
        """Delete the logo."""
        self._http.delete_logo([self.id])

class Icon(Asset):
    def __init__(self, payload: dict, http: HTTPClient) -> None:
        super().__init__(
            payload, 
            AssetType.Icon,
            http
        )
    
    def __repr__(self) -> str:
        return f'<Icon id={self.id} height={self.height} width={self.width} author={self.author.name}>'
    
    def delete(self) -> None:
        """Delete the icon."""
        self._http.delete_icon([self.id])