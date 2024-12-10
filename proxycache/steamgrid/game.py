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

from datetime import datetime
from typing import Iterator, Tuple, Any

__all__ = (
    'Game',
)

class Game:
    """Represents a custom game.

    Depending on the way this object was created, some of the attributes can
    have a value of ``None``.

    .. container:: operations
        .. describe:: x == y
            Checks if two game are the same.
        .. describe:: x != y
            Checks if two game are not the same.
        .. describe:: iter(x)
            Returns an iterator of ``(field, value)`` pairs. This allows this class
            to be used as an iterable in list/dict/etc constructions.
        .. describe:: str(x)
            Returns a string representation of the game.


    Attributes
    -----------
    name: :class:`str`
        The name of the game.
    id: :class:`int`
        The game's ID.
    types: List[:class:`str`]
        List of game types.
    verified: :class:`bool`
        Whether an game is verified or not.
    release_date: Optional[:class:`datetime`]
        The release date of the game.
    """

    __slots__ = (
        '_payload',
        'id',
        'name',
        'types',
        'verified',
        'release_date',
        '_release_date'
    )

    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self._from_data(payload)

    def _from_data(self, game: dict):
        self.name = game.get('name')
        self.id = game.get('id')
        self.types = game.get('types')
        self.verified = game.get('verified')
        self._release_date = game.get('release_date', None)
        self.release_date = datetime.fromtimestamp(game['release_date']) if self._release_date else None

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f'<Game id={self.id} name={self.name}>'

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
        """:class:`dict`: Returns a JSON-compatible representation of the author."""
        return self._payload