import os
import json
import re
import logging
import requests
from steamgriddba import SteamGridDB
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry, RateLimitException
from collections import defaultdict
import requests_cache
from urllib.parse import urlparse, parse_qs, unquote

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize cache with requests-cache
requests_cache.install_cache('steamgriddb_cache', expire_after=3600)  # 1 hour cache expiration

# SteamGridDB API key
API_KEY = os.getenv('STEAMGRIDDB_API_KEY')
sgdb = SteamGridDB(API_KEY)

# Rate-limiting parameters
RATE_LIMIT = 100
RATE_LIMIT_PERIOD = 60  # in seconds

# Initialize cache and IP rate-limiting tracking
api_cache = {}
ip_request_counts = defaultdict(int)
blocked_ips = set()

# Create a session with connection pooling and retries
session = requests.Session()
retry = requests.adapters.Retry(connect=3, backoff_factor=0.5)
adapter = requests.adapters.HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# FastAPI app setup
app = FastAPI()

@sleep_and_retry
@limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD)
def limited_request(url, headers):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response
    except RateLimitException as e:
        logger.error(f"Rate limit exceeded: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        raise

def sanitize_game_name(game_name):
    """Sanitize game name by removing special characters"""
    return re.sub(r'[^\w\s]', '', game_name)

def is_cache_valid(cache_entry):
    """Check if the cache entry is still valid"""
    return (datetime.now() - cache_entry['timestamp']).seconds < 3600

@app.get("/grid/{game_name}")
async def get_game_grid(game_name: str):
    """Get the grid image URL for a specific game"""
    sanitized_name = sanitize_game_name(game_name)

    # Check cache for the game grid
    if sanitized_name in api_cache and is_cache_valid(api_cache[sanitized_name]):
        logger.info(f"Serving from cache: {sanitized_name}")
        response = api_cache[sanitized_name]['data']
    else:
        # Fetch grid from SteamGridDB
        try:
            games = sgdb.search_game(sanitized_name)
            if games:
                grid_url = games[0].image_steam_grid
                response = {"game": sanitized_name, "grid_url": grid_url}
                # Cache the result
                api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
            else:
                # Fallback if no results found
                response = {"message": "Game not found."}
                api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
        except Exception as e:
            logger.error(f"Error fetching game grid: {e}")
            raise HTTPException(status_code=500, detail="Error fetching game grid")

    return response

@app.get("/search/{game_name}")
async def search_game(game_name: str):
    """Search for a game and get its ID"""
    sanitized_name = sanitize_game_name(game_name)

    # Decline certain terms
    decline_terms = ["NonSteamLaunchers", "Repair EA App", "Nexon Launcher", "RemotePlayWhatever"]
    if sanitized_name in decline_terms:
        raise HTTPException(status_code=400, detail="Search term is not allowed")

    # Check cache for search result
    if sanitized_name in api_cache and is_cache_valid(api_cache[sanitized_name]):
        logger.info(f"Serving search result from cache: {sanitized_name}")
        response = api_cache[sanitized_name]['data']
    else:
        try:
            games = sgdb.search_game(sanitized_name)
            if games:
                game_id = games[0].id
                response = {"data": [{"id": game_id}]}
                api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
            else:
                response = {"data": [], "message": "No results found."}
                api_cache[sanitized_name] = {'data': response, 'timestamp': datetime.now()}
        except Exception as e:
            logger.error(f"Error searching for game: {e}")
            raise HTTPException(status_code=500, detail="Error searching for game")

    return response

# Optional route to check cache status
@app.get("/cache_status")
async def cache_status():
    """Check cache expiration status"""
    if requests_cache.is_cache_expired('steamgriddb_cache'):
        return {"status": "Cache expired. Refreshing..."}
    else:
        return {"status": "Using cached response."}

    httpd = server_class(server_address, handler_class)
    logger.info(f'Starting proxy cache server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
