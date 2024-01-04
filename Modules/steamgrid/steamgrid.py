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

from typing import List, Optional

from .http import HTTPClient
from .game import Game
from .enums import (
    StyleType, 
    MimeType, 
    ImageType,
    PlatformType
)
from .asset import *

__all__ = (
    'SteamGridDB',
)

class SteamGridDB:
    """Represents a custom author.

    Attributes
    -----------
    auth_key: :class:`str`
        The auth key of the steamgriddb for authorization.
    
    """

    __slots__ = ('_http')

    def __init__(self, auth_key: str) -> None:
        self._http = HTTPClient(auth_key)

    def auth_key(self) -> str:
        """:class:`str`: Returns the auth key of the steamgriddb.
        
        Returns
        --------
        :class:`str`
            The auth key of the steamgriddb.
        """
        return self._http.auth_key

    def get_game_by_gameid(
        self,
        game_id: int,
    ) -> Optional[Game]:
        """:class:`Game`: Returns a game by game id.
        
        Parameters
        -----------
        game_id: :class:`int`
            The game id of the game.

        Raises
        --------
        TypeError
            If the game_id is not an integer.
        HTTPException
            If the game_id is not found.

        Returns
        --------
        :class:`Game`
            The game that was fetched.
        """
        if not isinstance(game_id, int):
            raise TypeError('\'game_id\' must be an integer.')

        payload = self._http.get_game(game_id, 'game')
        return Game(payload) if payload != [] else None

    def get_game_by_steam_appid(
        self,
        app_id: int,
    ) -> Optional[Game]:
        """:class:`Game`: Returns a game by steam app id.

        Parameters
        -----------
        app_id: :class:`int`
            The steam app id of the game.

        Raises
        --------
        TypeError
            If the app_id is not an integer.
        HTTPException
            If the app_id is not found.

        Returns
        --------
        :class:`Game`
            The game that was fetched.
        """
        if not isinstance(app_id, int):
            raise TypeError('\'app_id\' must be an integer.')

        payload = self._http.get_game(app_id, 'steam')
        return Game(payload) if payload != [] else None
    
    def get_grids_by_gameid(
        self,
        game_ids: List[int],
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Grid]]:
        """Optional[List[:class:`Grid`]] Returns a list of grids by game id.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        styles: List[:class:`StyleType`]
            The styles of the grids. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the grids. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the grids. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the grids are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the grids are humor. Defaults to False.

        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If the game_id is not found.
        
        Returns
        --------
        Optional[List[:class:`Grid`]]
            The grids that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')
    
        queries = {
            'styles': ','.join(i.value for i in styles),
            'mimes': ','.join(i.value for i in mimes),
            'types': ','.join(i.value for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }
        payloads = self._http.get_grid(game_ids, 'game', queries=queries)
        if payloads != []:
            return [Grid(payload, self._http) for payload in payloads]
        return None

    def get_grids_by_platform(
        self,
        game_ids: List[int],
        platform: PlatformType,
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Grid]]:

        """Optional[List[:class:`Grid`]] Returns a list of grids by platform.
        
        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        platform: :class:`PlatformType`
            The platform type of the grids.
        styles: List[:class:`StyleType`]
            The styles of the grids. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the grids. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the grids. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the grids are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the grids are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.

        Returns
        --------
        Optional[List[:class:`Grid`]]
            The grids that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(platform, PlatformType):
            raise TypeError('\'platform\' must be a PlatformType.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(str(i) for i in styles),
            'mimes': ','.join(str(i) for i in mimes),
            'types': ','.join(str(i) for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_grid(
            game_ids,
            'platform', 
            platform=platform.value, 
            queries=queries
        )
        if payloads != []:
            return [Grid(payload, self._http) for payload in payloads]
        return None

    def get_heroes_by_gameid(
        self,
        game_ids: List[int],
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Hero]]:
        """Optional[List[:class:`Hero`]] Returns a list of heroes by game id.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        styles: List[:class:`StyleType`]
            The styles of the heroes. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the heroes. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the heroes. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the heroes are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the heroes are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.

        Returns
        --------
        Optional[List[:class:`Hero`]]
            The heroes that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(i.value for i in styles),
            'mimes': ','.join(i.value for i in mimes),
            'types': ','.join(i.value for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_hero(game_ids, 'game', queries=queries)
        if payloads != []:
            return [Hero(payload, self._http) for payload in payloads]
        return None
    
    def get_heroes_by_platform(
        self,
        game_ids: List[int],
        platform: PlatformType,
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Hero]]:
        """Optional[List[:class:`Hero`]] Returns a list of heroes by platform.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        platform: :class:`PlatformType`
            The platform type of the heroes.
        styles: List[:class:`StyleType`]
            The styles of the heroes. Defaults to all styles.
        mimes: List[:class:`MimeType`] 
            The mimes of the heroes. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the heroes. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the heroes are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the heroes are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        
        Returns
        --------
        Optional[List[:class:`Hero`]]
            The heroes that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(platform, PlatformType):
            raise TypeError('\'platform\' must be a PlatformType.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(str(i) for i in styles),
            'mimes': ','.join(str(i) for i in mimes),
            'types': ','.join(str(i) for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_hero(
            game_ids, 
            'platform', 
            platform=platform.value, 
            queries=queries
        )
        if payloads != []:
            return [Grid(payload, self._http) for payload in payloads]
        return None

    def get_logos_by_gameid(
        self,
        game_ids: List[int],
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Logo]]:
        """Optional[List[:class:`Logo`]] Returns a list of logos by game id.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        styles: List[:class:`StyleType`]
            The styles of the logos. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the logos. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the logos. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the logos are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the logos are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        
        Returns
        --------
        Optional[List[:class:`Logo`]]
            The logos that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(i.value for i in styles),
            'mimes': ','.join(i.value for i in mimes),
            'types': ','.join(i.value for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_logo(game_ids, 'game', queries=queries)
        if payloads != []:
            return [Logo(payload, self._http) for payload in payloads]
        return None
    
    def get_logos_by_platform(
        self,
        game_ids: List[int],
        platform: PlatformType,
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Logo]]:
        """Optional[List[:class:`Logo`]] Returns a list of logos by platform.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        platform: :class:`PlatformType`
            The platform type of the logos.
        styles: List[:class:`StyleType`]
            The styles of the logos. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the logos. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the logos. Defaults to all types.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(platform, PlatformType):
            raise TypeError('\'platform\' must be a PlatformType.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(str(i) for i in styles),
            'mimes': ','.join(str(i) for i in mimes),
            'types': ','.join(str(i) for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_logo(
            game_ids, 
            'platform', 
            platform=platform.value, 
            queries=queries
        )
        if payloads != []:
            return [Logo(payload, self._http) for payload in payloads]
        return None

    def get_icons_by_gameid(
        self,
        game_ids: List[int],
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Icon]]:
        """Optional[List[:class:`Icon`]] Returns a list of icons by game id.
        
        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        styles: List[:class:`StyleType`]
            The styles of the icons. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the icons. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the icons. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the icons are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the icons are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.

        Returns
        --------
        Optional[List[:class:`Icon`]]
            The icons that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(i.value for i in styles),
            'mimes': ','.join(i.value for i in mimes),
            'types': ','.join(i.value for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_icon(game_ids, 'game', queries=queries)
        if payloads != []:
            return [Icon(payload, self._http) for payload in payloads]
        return None
    
    def get_icons_by_platform(
        self,
        game_ids: List[int],
        platform: PlatformType,
        styles: List[StyleType] = [],
        mimes: List[MimeType] = [],
        types: List[ImageType] = [],
        is_nsfw: bool = False,
        is_humor: bool = False,
    ) -> Optional[List[Icon]]:
        """Optional[List[:class:`Icon`]] Returns a list of icons by platform.

        Parameters
        -----------
        game_ids: List[:class:`int`]
            The game ids of the games.
        platform: :class:`PlatformType`
            The platform type of the icons.
        styles: List[:class:`StyleType`]
            The styles of the icons. Defaults to all styles.
        mimes: List[:class:`MimeType`]
            The mimes of the icons. Defaults to all mimes.
        types: List[:class:`ImageType`]
            The types of the icons. Defaults to all types.
        is_nsfw: :class:`bool`
            Whether or not the icons are NSFW. Defaults to False.
        is_humor: :class:`bool`
            Whether or not the icons are humor. Defaults to False.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        
        Returns
        --------
        Optional[List[:class:`Icon`]]
            The icons that were fetched.
        """
        if not isinstance(game_ids, List):
            raise TypeError('\'game_ids\' must be a list of integers.')
        if not isinstance(platform, PlatformType):
            raise TypeError('\'platform\' must be a PlatformType.')
        if not isinstance(styles, List):
            raise TypeError('\'styles\' must be a list of StyleType.')
        if not isinstance(mimes, List):
            raise TypeError('\'mimes\' must be a list of MimeType.')
        if not isinstance(types, List):
            raise TypeError('\'types\' must be a list of ImageType.')
        if not isinstance(is_nsfw, bool):
            raise TypeError('\'is_nsfw\' must be a boolean.')
        if not isinstance(is_humor, bool):
            raise TypeError('\'is_humor\' must be a boolean.')

        queries = {
            'styles': ','.join(str(i) for i in styles),
            'mimes': ','.join(str(i) for i in mimes),
            'types': ','.join(str(i) for i in types),
            'nsfw': str(is_nsfw).lower(),
            'humor': str(is_humor).lower(),
        }

        payloads = self._http.get_icon(
            game_ids, 
            'platform', 
            platform=platform.value, 
            queries=queries
        )
        if payloads != []:
            return [Icon(payload, self._http) for payload in payloads]
        return None

    def delete_grid(
        self,
        grid_ids: List[int],
    ) -> None:
        """Deletes list of grid images from the website.

        Parameters
        -----------
        grid_ids: List[:class:`int`]
            The grid ids to delete.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        """
        if not isinstance(grid_ids, List):
            raise TypeError('\'grid_ids\' must be a list of integers.')

        self._http.delete_grid(grid_ids)
    
    def delete_hero(
        self,
        hero_ids: List[int],
    ) -> None:
        """Deletes list of hero images from the website.

        Parameters
        -----------
        hero_ids: List[:class:`int`]
            The hero ids to delete.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        """
        if not isinstance(hero_ids, List):
            raise TypeError('\'hero_ids\' must be a list of integers.')

        self._http.delete_hero(hero_ids)
    
    def delete_logo(
        self,
        logo_ids: List[int],
    ) -> None:
        """Deletes list of logo images from the website.

        Parameters
        -----------
        logo_ids: List[:class:`int`]
            The logo ids to delete.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        """
        if not isinstance(logo_ids, List):
            raise TypeError('\'logo_ids\' must be a list of integers.')

        self._http.delete_logo(logo_ids)
    
    def delete_icon(
        self,
        icon_ids: List[int],
    ) -> None:
        """Deletes list of icon images from the website.

        Parameters
        -----------
        icon_ids: List[:class:`int`]
            The icon ids to delete.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        """
        if not isinstance(icon_ids, List):
            raise TypeError('\'icon_ids\' must be a list of integers.')

        self._http.delete_icon(icon_ids)

    def search_game(
        self, 
        term: str
    ) -> Optional[List[Game]]:
        """Searches for games on the website.
        
        Parameters
        -----------
        term: :class:`str`
            The term to search for.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        
        Returns
        --------
        Optional[List[:class:`Game`]]
            The list of games that match the search term.
        """
        if not isinstance(term, str):
            raise TypeError('\'term\' must be a string.')

        payloads = self._http.search_games(term)
        return [Game(payload) for payload in payloads]

    def set_auth_key(
        self, 
        auth_key: str
    ) -> None:
        """Sets the new auth key for the API.

        Parameters
        -----------
        auth_key: :class:`str`
            The new auth key to set.
        
        Raises
        --------
        TypeError
            If one of the parameters is not of the correct type.
        HTTPException
            If there is an error with the request.
        ValueError
            If the auth key is not valid format.
        """
        if not isinstance(auth_key, str):
            raise TypeError('\'auth_key\' must be a string.')
        if len(auth_key) != 32:
            raise ValueError('\'auth_key\' must be a 32-character string.')

        self._http.session.headers['Authorization'] = f'Bearer {auth_key}'