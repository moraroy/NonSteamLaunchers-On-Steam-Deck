import json
import os
import re
import requests
from steamgrid import SteamGridDB
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
from ratelimit import limits, sleep_and_retry, RateLimitException
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from steamgrid.enums import PlatformType
from datetime import datetime, timedelta
import logging
import time

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize an empty dictionary to serve as the cache
api_cache = {}

# API Key for SteamGridDB
API_KEY = os.getenv('STEAMGRIDDB_API_KEY')
sgdb = SteamGridDB(API_KEY)  # Create an instance of SteamGridDB

# Define rate limit (e.g., 100 requests per minute)
RATE_LIMIT = 100
RATE_LIMIT_PERIOD = 60  # in seconds

# Create a session with connection pooling
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

@sleep_and_retry
@limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD)
def limited_request(url, headers):
    try:
        # Set a timeout to prevent long hanging connections
        response = session.get(url, headers=headers, timeout=10)  # Timeout set to 10 seconds
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        return response
    except RateLimitException as e:
        logger.error(f"Rate limit exceeded: {e}")
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f"Request timed out: {e}")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        # Handles all other request errors
        logger.error(f"Request error: {e}")
        raise
    except requests.exceptions.RemoteDisconnected as e:
        logger.error(f"Remote disconnected: {e}")
        # Optionally retry after a short delay, or log the issue and return None
        time.sleep(2)  # Retry after 2 seconds or use exponential backoff
        return limited_request(url, headers)  # Retry the request

def sanitize_game_name(game_name):
    # Remove special characters like ™ and ®
    sanitized_name = re.sub(r'[^\w\s]', '', game_name)
    return sanitized_name

class ProxyCacheHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        logger.info(f"Parsed path: {parsed_path.path}")
        logger.info(f"Path parts: {path_parts}")

        if len(path_parts) < 2 or path_parts[1] == '':
            # Handle the root path ('/')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Welcome to the Proxy Cache Server!')
            return

        if path_parts[1] == 'search':
            game_name = unquote(path_parts[2])  # Decode the URL-encoded game name
            self.handle_search(game_name)
        else:
            if len(path_parts) < 4:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid request')
                return

            art_type = path_parts[1]
            game_id = path_parts[3]
            dimensions = parse_qs(parsed_path.query).get('dimensions', [None])[0]

            logger.info(f"Art type: {art_type}")
            logger.info(f"Game ID: {game_id}")
            logger.info(f"Dimensions: {dimensions}")

            self.handle_artwork(game_id, art_type, dimensions)

    def do_HEAD(self):
        self.do_GET()  
        self.send_response(200)  
        self.end_headers()
        logger.info(f"HEAD request handled for: {self.path}")

    def do_OPTIONS(self):
        self.send_response(200)  # OK status
        self.send_header('Allow', 'GET, POST, HEAD, OPTIONS') 
        self.end_headers()
        logger.info(f"OPTIONS request handled for: {self.path}")

    def handle_search(self, game_name):
        logger.info(f"Searching for game ID for: {game_name}")

        # List of terms to decline
        decline_terms = ["NonSteamLaunchers", "Repair EA App", "Nexon Launcher", "RemotePlayWhatever"]

        if game_name in decline_terms:
            logger.info(f"Declining search for: {game_name}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Search term is not allowed')
            return

        try:
            sanitized_name = sanitize_game_name(game_name)
            logger.info(f"Sanitized game name: {sanitized_name}")

            # Check if the search term is in the cache
            if sanitized_name in api_cache and self.is_cache_valid(api_cache[sanitized_name]):
                logger.info(f"Serving from cache: {sanitized_name}")
                response = api_cache[sanitized_name]['data']
            else:
                games = sgdb.search_game(sanitized_name)
                if games:
                    game_id = games[0].id
                    response = {'data': [{'id': game_id}]}
                    # Store the search term and response in the cache
                    api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
                else:
                    # Fallback to Steam platform if no results from SteamGridDB
                    fallback_results = self.search_fallback_platforms(sanitized_name)
                    if fallback_results:
                        response = {'data': fallback_results}
                        # Store the search term and response in the cache
                        api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
                    else:
                        response = {'data': [], 'message': 'No artwork found for the given search term.'}
                        # Store the search term and response in the cache
                        api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            logger.error(f"Error searching for game ID: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Error searching for game ID')

    def search_fallback_platforms(self, game_name):
        fallback_results = []
        steam_results = self.search_steamgridb(game_name)
        if steam_results:
            fallback_results.extend(steam_results)
        return fallback_results

    def search_steamgridb(self, game_name):
        try:
            games = sgdb.search_game(game_name)
            if games:
                return [{'id': game.id, 'name': game.name} for game in games]
        except Exception as e:
            logger.error(f"Error searching SteamGridDB: {e}")
        return []

    def handle_artwork(self, game_id, art_type, dimensions):
        if not game_id:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Game ID is required')
            return

        logger.info(f"Downloading {art_type} artwork for game ID: {game_id}")
        cache_key = (game_id, art_type, dimensions)
        if cache_key in api_cache and self.is_cache_valid(api_cache[cache_key]):
            logger.info(f"Serving from cache: {cache_key}")
            data = api_cache[cache_key]['data']
        else:
            try:
                url = f"https://www.steamgriddb.com/api/v2/{art_type}/game/{game_id}"
                if dimensions:
                    url += f"?dimensions={dimensions}"

                # Check for specific game IDs and request alternate artwork styles
                if game_id in ['5260961', '5297303']:
                    url += "&style=alternate"

                headers = {'Authorization': f'Bearer {API_KEY}'}
                logger.info(f"Sending request to: {url}")
                response = limited_request(url, headers)
                data = response.json()
                api_cache[cache_key] = {'data': data, 'timestamp': datetime.now()}
                logger.info(f"Storing in cache: {cache_key}")
            except Exception as e:
                logger.error(f"Error making API call: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error fetching artwork')
                return

        # Send the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def is_cache_valid(self, cached_item):
        expiration_time = timedelta(hours=1)
        return datetime.now() - cached_item['timestamp'] < expiration_time


def run(server_class=HTTPServer, handler_class=ProxyCacheHandler):
    port = int(os.environ.get('PORT', 8000))  # Use the environment variable PORT or default to 8000
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f'Starting proxy cache server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
