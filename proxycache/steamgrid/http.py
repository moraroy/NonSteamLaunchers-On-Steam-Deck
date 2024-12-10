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

import requests
from typing import List

class HTTPException(Exception):
    """Exception raised when the HTTP request fails."""
    pass

class HTTPClient:

    BASE_URL = 'https://www.steamgriddb.com/api/v2'

    def __init__(self, auth_key: str):
        self.session = requests.Session()
        self.auth_key = auth_key
        self.session.headers.update({'Authorization': 'Bearer ' + self.auth_key})

    def get(self, endpoint: str, queries: dict = None) -> dict:
        if queries:
            responce = self.session.get(endpoint, params=queries)
        else:
            responce = self.session.get(endpoint)

        try: 
            payload = responce.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception('Responce JSON Decode Error')

        if not payload['success']:
            error_context = payload['errors'][0]
            raise HTTPException(f'API Error: ({responce.status_code}) {error_context}')

        return payload['data'] if payload else None

    def post(self, endpoint: str, body: dict = None) -> dict:
        responce = self.session.post(endpoint, data=body)
        try: 
            payload = responce.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception('Responce JSON Decode Error')

        is_success = payload.get('success', None)
        if not is_success:
            error_context = payload['errors'][0] if payload else ''
            raise HTTPException(f'API Error: ({responce.status_code}) {error_context}')

        return payload['data'] if payload else None
    
    def delete(self, endpoint: str) -> dict:
        responce = self.session.delete(endpoint)
        try: 
            payload = responce.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception('Responce JSON Decode Error')

        if not payload['success']:
            error_context = payload['errors'][0]
            raise HTTPException(f'API Error: ({responce.status_code}) {error_context}')

        return payload['data'] if payload else None

    def get_game(self, game_id: int, request_type: str) -> dict:
        if request_type == 'steam':
            url = self.BASE_URL + '/games/steam/' + str(game_id)
        elif request_type == 'game':
            url = self.BASE_URL + '/games/id/' + str(game_id)

        return self.get(url)

    def get_grid(
        self, 
        game_ids: List[int], 
        request_type: str, 
        platform: str = None, 
        queries: dict = None
    ) -> List[dict]:
        if request_type == 'game':
            url = self.BASE_URL + '/grids/game/' + str(game_ids[0])
        elif request_type == 'platform':
            url = self.BASE_URL + '/grids/' + platform + '/' + ','.join(str(i) for i in game_ids)

        return self.get(url, queries)

    def delete_grid(self, grid_ids: List[int]):
        url = self.BASE_URL + '/grids/' + ','.join(str(i) for i in grid_ids)
        self.delete(url)
    
    def get_hero(
        self, 
        game_ids: List[int], 
        request_type: str, 
        platform: str = None, 
        queries: dict = None
    ) -> List[dict]:
        if request_type == 'game':
            url = self.BASE_URL + '/heroes/game/' + str(game_ids[0])
        elif request_type == 'platform':
            url = self.BASE_URL + '/heroes/' + platform + '/' + ','.join(str(i) for i in game_ids)

        return self.get(url, queries)

    def delete_hero(self, hero_ids: List[int]):
        url = self.BASE_URL + '/heroes/' + ','.join(str(i) for i in hero_ids)
        self.delete(url)
    
    def get_logo(
        self, 
        game_ids: List[int], 
        request_type: str, 
        platform: str = None, 
        queries: dict = None
    ) -> List[dict]:
        if request_type == 'game':
            url = self.BASE_URL + '/logos/game/' + str(game_ids[0])
        elif request_type == 'platform':
            url = self.BASE_URL + '/logos/' + platform + '/' + ','.join(str(i) for i in game_ids)

        return self.get(url, queries)

    def delete_logo(self, logo_ids: List[int]):
        url = self.BASE_URL + '/logos/' + ','.join(str(i) for i in logo_ids)
        self.delete(url)
    
    def get_icon(self, game_ids: List[int], request_type: str, platform: str = None, queries: dict = None) -> List[dict]:
        if request_type == 'game':
            url = self.BASE_URL + '/icons/game/' + str(game_ids[0])
        elif request_type == 'platform':
            url = self.BASE_URL + '/icons/' + platform + '/' + ','.join(str(i) for i in game_ids)

        return self.get(url, queries)

    def delete_icon(self, logo_ids: List[int]):
        url = self.BASE_URL + '/icons/' + ','.join(str(i) for i in logo_ids)
        self.delete(url)

    def search_games(self, term: str) -> List[dict]:
        url = self.BASE_URL + '/search/autocomplete/' + term

        return self.get(url)