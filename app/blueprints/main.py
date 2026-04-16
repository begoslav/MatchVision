from flask import Blueprint, render_template, request, jsonify
from app.services import api_service
from app.services.api_service import _current_season

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage with featured league standings"""
    # La Liga (140), Ligue 1 (61), Premier League (39)
    featured_ids = [140, 61, 39]
    featured_leagues = []
    for lid in featured_ids:
        data = api_service.get_league_standings_with_info(lid)
        if data:
            featured_leagues.append(data)

    return render_template('index.html', featured_leagues=featured_leagues)

@main_bp.route('/api/live-matches')
def live_matches():
    """API endpoint for live matches"""
    matches = api_service.get_live_matches()
    return jsonify({'matches': matches, 'count': len(matches)})

@main_bp.route('/leagues')
def leagues():
    """View leagues"""
    leagues_data = api_service.get_top_leagues()
    return render_template('leagues.html', leagues=leagues_data)

@main_bp.route('/league/<int:league_id>')
def league_standings(league_id):
    """View league standings"""
    season = request.args.get('season', _current_season(), type=int)
    standings = api_service.get_league_standings(league_id, season)
    return render_template('league_standings.html', standings=standings, league_id=league_id, season=season)
