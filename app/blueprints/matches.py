from flask import Blueprint, render_template, jsonify
from app.services import api_service, summary_service

matches_bp = Blueprint('matches', __name__, url_prefix='/matches')

@matches_bp.route('/live')
def live():
    """View live matches"""
    matches = api_service.get_live_matches()
    return render_template('matches/live.html', matches=matches)

@matches_bp.route('/<int:match_id>')
def detail(match_id):
    """Match detail page with statistics and summary"""
    match_data = api_service.get_match_details(match_id)
    
    if not match_data:
        return render_template('matches/detail.html', match_data=None, summary=None, lineups=[]), 404
    
    lineups = api_service.get_match_lineups(match_id)
    ratings = api_service.get_match_player_ratings(match_id)
    summary = summary_service.generate_match_summary(match_data)
    
    return render_template('matches/detail.html', match_data=match_data, summary=summary, lineups=lineups, ratings=ratings)

@matches_bp.route('/<int:match_id>/summary')
def get_summary(match_id):
    """API endpoint to get match summary"""
    match_data = api_service.get_match_details(match_id)
    
    if not match_data:
        return jsonify({'success': False, 'message': 'Match not found'}), 404
    
    summary = summary_service.generate_match_summary(match_data)
    
    return jsonify({
        'success': True,
        'summary': summary,
        'match_id': match_id
    })
