import requests
import os
import datetime
import hashlib
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def _current_season() -> int:
    """Return current football season year.
    European seasons start in July/August, so:
      - Jan–June 2026 → season 2025
      - July–Dec 2026 → season 2026
    """
    today = datetime.date.today()
    return today.year if today.month >= 7 else today.year - 1

# TTL in seconds for each endpoint pattern
CACHE_TTL = {
    '/fixtures/statistics': 300,    # 5 min (live) / effectively forever for FT
    '/fixtures/lineups':    300,    # 5 min
    '/fixtures':            60,     # 60 s for live; team history gets 1h below
    '/standings':           3600,   # 1 h
    '/leagues':             86400,  # 24 h
    '/teams/statistics':    21600,  # 6 h
    '/teams':               86400,  # 24 h
}

def _cache_ttl(endpoint: str, params: Dict) -> int:
    """Return appropriate TTL based on endpoint and params."""
    if endpoint == '/fixtures':
        if params and params.get('live'):
            return 60           # live feed — 60 s
        if params and params.get('status') in ('FT', 'NS'):
            return 3600         # finished/scheduled team fixtures — 1 h
        if params and params.get('id'):
            return 300          # single match detail — 5 min
        return 3600
    if endpoint in ('/fixtures/statistics', '/fixtures/lineups'):
        return 300
    return CACHE_TTL.get(endpoint, 600)

class APIFootballService:
    """Service for API-Football integration"""
    
    def __init__(self):
        self.api_key = os.getenv('API_FOOTBALL_KEY')
        self.base_url = 'https://v3.football.api-sports.io'
        self.headers = {
            'x-apisports-key': self.api_key
        }
        self.timeout = 10
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make request to API-Football with SQLite caching."""
        if not self.api_key:
            logger.error("API key not configured")
            return None

        # Build cache key
        param_str = '&'.join(f"{k}={v}" for k, v in sorted((params or {}).items()))
        raw_key = f"{endpoint}?{param_str}"
        cache_key = hashlib.md5(raw_key.encode()).hexdigest()

        # Try cache first
        try:
            from app.models import ApiCache
            cached = ApiCache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache HIT: {raw_key}")
                return cached
        except Exception as e:
            logger.warning(f"Cache read failed: {e}")

        # Cache miss — call API
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None

        # Store in cache
        try:
            from app.models import ApiCache
            ttl = _cache_ttl(endpoint, params or {})
            ApiCache.set(cache_key, data, ttl)
            logger.debug(f"Cache SET ({ttl}s): {raw_key}")
        except Exception as e:
            logger.warning(f"Cache write failed: {e}")

        return data
    
    def get_live_matches(self) -> List[Dict]:
        """Get all live matches"""
        response = self._make_request('/fixtures', params={'live': 'all'})
        if response and 'response' in response:
            return response['response']
        return []
    
    def get_league_standings(self, league_id: int, season: int) -> List[Dict]:
        """Get league standings table"""
        response = self._make_request('/standings', params={
            'league': league_id,
            'season': season
        })
        
        if response and 'response' in response and len(response['response']) > 0:
            standings = response['response'][0]
            if 'league' in standings and 'standings' in standings['league']:
                return standings['league']['standings'][0] if standings['league']['standings'] else []
        return []

    def get_all_standings_groups(self, league_id: int, season: int) -> List[Dict]:
        """Get all standing groups (for cups with multiple groups like CL).
        Returns list of {'name': str, 'standings': List[Dict]}
        """
        response = self._make_request('/standings', params={
            'league': league_id,
            'season': season
        })
        if response and 'response' in response and response['response']:
            data = response['response'][0]
            if 'league' in data and 'standings' in data['league']:
                groups = []
                for i, group in enumerate(data['league']['standings']):
                    name = group[0].get('group', f'Skupina {i+1}') if group else f'Skupina {i+1}'
                    groups.append({'name': name, 'standings': group})
                return groups
        return []
    
    def get_team_details(self, team_id: int) -> Optional[Dict]:
        """Get team details"""
        response = self._make_request('/teams/statistics', params={
            'team': team_id,
            'season': _current_season()
        })
        
        if response and 'response' in response:
            return response['response']
        return None
    
    def get_team_info(self, team_id: int) -> Optional[Dict]:
        """Get basic team information"""
        response = self._make_request('/teams', params={'id': team_id})
        
        if response and 'response' in response and len(response['response']) > 0:
            return response['response'][0]
        return None
    
    def get_match_details(self, match_id: int) -> Optional[Dict]:
        """Get detailed match information including statistics"""
        response = self._make_request('/fixtures', params={'id': match_id})
        
        if not response or 'response' not in response or len(response['response']) == 0:
            return None
        
        match = response['response'][0]
        
        # Fetch statistics separately
        stats_response = self._make_request('/fixtures/statistics', params={'fixture': match_id})
        if stats_response and 'response' in stats_response:
            match['statistics'] = stats_response['response']
        else:
            match['statistics'] = []
        
        return match
    
    def get_match_lineups(self, match_id: int) -> List[Dict]:
        """Get team lineups for a match"""
        response = self._make_request('/fixtures/lineups', params={'fixture': match_id})
        if response and 'response' in response:
            return response['response']
        return []

    def search_teams(self, query: str) -> List[Dict]:
        """Search for teams by name"""
        if not query or len(query) < 2:
            return []
        
        response = self._make_request('/teams', params={'search': query})
        
        if response and 'response' in response:
            return response['response'][:15]  # Limit to 15 results
        return []
    
    def get_team_matches(self, team_id: int, season: int = None, limit: int = 10) -> List[Dict]:
        """Get team's recent finished matches."""
        today = datetime.date.today()
        use_season = season or _current_season()
        date_from = (today - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        date_to = today.strftime('%Y-%m-%d')
        response = self._make_request('/fixtures', params={
            'team': team_id,
            'season': use_season,
            'from': date_from,
            'to': date_to,
            'status': 'FT'
        })
        if response and 'response' in response:
            matches = response['response']
            # Sort newest first and limit
            matches.sort(key=lambda m: m['fixture']['date'], reverse=True)
            return matches[:limit]
        return []

    def get_upcoming_matches(self, team_id: int, limit: int = 5) -> List[Dict]:
        """Get team's upcoming matches using date range"""
        today = datetime.date.today()
        date_to = (today + datetime.timedelta(days=60)).strftime('%Y-%m-%d')
        date_from = today.strftime('%Y-%m-%d')
        response = self._make_request('/fixtures', params={
            'team': team_id,
            'season': _current_season(),
            'from': date_from,
            'to': date_to,
            'status': 'NS'
        })
        if response and 'response' in response:
            matches = response['response']
            matches.sort(key=lambda m: m['fixture']['date'])
            return matches[:limit]
        return []
    
    def compare_teams(self, team1_id: int, team2_id: int, season: int = None) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Get statistics for comparing two teams"""
        team1_stats = self.get_team_details(team1_id)
        team2_stats = self.get_team_details(team2_id)
        return team1_stats, team2_stats
    
    def get_league_info(self, league_id: int, season: int = None) -> Optional[Dict]:
        """Get basic league/cup info (name, logo, country) without standings."""
        response = self._make_request('/leagues', params={
            'id': league_id,
            'season': season or _current_season()
        })
        if response and 'response' in response and response['response']:
            item = response['response'][0]
            return {
                'id': item['league']['id'],
                'name': item['league']['name'],
                'logo': item['league']['logo'],
                'country': item.get('country', {}).get('name', 'Europe'),
            }
        return None

    def get_league_standings_with_info(self, league_id: int, season: int = None) -> Optional[Dict]:
        """Get league info (name, logo) together with standings for a specific league."""
        response = self._make_request('/standings', params={
            'league': league_id,
            'season': season or _current_season()
        })
        if response and 'response' in response and len(response['response']) > 0:
            data = response['response'][0]
            if 'league' in data and 'standings' in data['league']:
                return {
                    'id': data['league']['id'],
                    'name': data['league']['name'],
                    'logo': data['league']['logo'],
                    'country': data['league'].get('country', ''),
                    'standings': data['league']['standings'][0] if data['league']['standings'] else []
                }
        return None

    def get_league_rounds(self, league_id: int, season: int = None) -> List[str]:
        """Get all rounds for a league/cup."""
        response = self._make_request('/fixtures/rounds', params={
            'league': league_id,
            'season': season or _current_season()
        })
        if response and 'response' in response:
            return response['response']
        return []

    def get_fixtures_by_round(self, league_id: int, round_name: str, season: int = None) -> List[Dict]:
        """Get all fixtures for a specific round."""
        response = self._make_request('/fixtures', params={
            'league': league_id,
            'season': season or _current_season(),
            'round': round_name
        })
        if response and 'response' in response:
            return response['response']
        return []

    def get_knockout_bracket(self, league_id: int, season: int = None) -> Dict:
        """Get knockout stage rounds and their fixtures for a cup competition."""
        # Rounds considered knockout (filter out group stages)
        knockout_keywords = ['round of', 'quarter', 'semi', 'final', '16', '32', '64']
        all_rounds = self.get_league_rounds(league_id, season)
        knockout_rounds = [
            r for r in all_rounds
            if any(kw in r.lower() for kw in knockout_keywords)
        ]
        result = {}
        for round_name in knockout_rounds:
            fixtures = self.get_fixtures_by_round(league_id, round_name, season)
            if fixtures:
                result[round_name] = fixtures
        return result
        """Get top domestic football leagues"""
        response = self._make_request('/leagues', params={'type': 'league'})
        
        if response and 'response' in response:
            major_leagues = [
                l for l in response['response']
                if l['league']['id'] in [39, 140, 78, 61, 71, 88, 94, 179, 207, 218]
            ]
            return major_leagues[:10]
        return []

    def get_top_leagues(self) -> List[Dict]:
        """Get top domestic football leagues"""
        response = self._make_request('/leagues', params={'type': 'league'})
        if response and 'response' in response:
            major_leagues = [
                l for l in response['response']
                if l['league']['id'] in [39, 140, 78, 61, 71, 88, 94, 179, 207, 218]
            ]
            return major_leagues[:10]
        return []

    def get_european_competitions(self) -> List[Dict]:
        result = []
        for lid, name, logo in [
            (2,   'UEFA Champions League', 'https://media.api-sports.io/football/leagues/2.png'),
            (3,   'UEFA Europa League',    'https://media.api-sports.io/football/leagues/3.png'),
            (848, 'UEFA Conference League','https://media.api-sports.io/football/leagues/848.png'),
        ]:
            result.append({
                'league': {'id': lid, 'name': name, 'logo': logo},
                'country': {'name': 'Europe'}
            })
        return result

# Create singleton instance
api_service = APIFootballService()
