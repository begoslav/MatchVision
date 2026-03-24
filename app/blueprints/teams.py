from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services import api_service, summary_service
from app.models import db, FavoriteTeam

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/search')
def search():
    """Search teams"""
    query = request.args.get('q', '').strip()
    teams = []
    
    if len(query) >= 2:
        teams = api_service.search_teams(query)
    
    return render_template('teams/search.html', teams=teams, query=query)

@teams_bp.route('/<int:team_id>')
def detail(team_id):
    """Team detail page"""
    team_info = api_service.get_team_info(team_id)
    team_stats = api_service.get_team_details(team_id)
    recent_matches = api_service.get_team_matches(team_id, limit=10)
    upcoming_matches = api_service.get_upcoming_matches(team_id, limit=5)
    
    # Check if favorited
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = FavoriteTeam.query.filter_by(
            user_id=current_user.id, 
            team_id=team_id
        ).first() is not None
    
    return render_template('teams/detail.html', 
                         team_id=team_id,
                         team_info=team_info,
                         team_stats=team_stats,
                         recent_matches=recent_matches,
                         upcoming_matches=upcoming_matches,
                         is_favorite=is_favorite)

@teams_bp.route('/compare')
def compare():
    """Compare two teams"""
    team1_id = request.args.get('team1', type=int)
    team2_id = request.args.get('team2', type=int)
    
    teams_to_display = []
    stats = {}
    
    if team1_id:
        teams_to_display.append(api_service.get_team_info(team1_id))
        stats[team1_id] = api_service.get_team_details(team1_id)
    
    if team2_id:
        teams_to_display.append(api_service.get_team_info(team2_id))
        stats[team2_id] = api_service.get_team_details(team2_id)
    
    return render_template('teams/compare.html', 
                         teams=teams_to_display,
                         team1_id=team1_id,
                         team2_id=team2_id,
                         stats=stats)

@teams_bp.route('/<int:team_id>/favorite', methods=['POST'])
@login_required
def add_favorite(team_id):
    """Add team to favorites"""
    try:
        # Check if already favorited
        existing = FavoriteTeam.query.filter_by(
            user_id=current_user.id,
            team_id=team_id
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Tým je již v oblíbených.'}), 400
        
        # Use data sent from frontend; fallback to API if missing
        data = request.get_json(silent=True) or {}
        team_name = data.get('team_name') or ''
        team_logo = data.get('team_logo') or ''
        
        if not team_name:
            team_info = api_service.get_team_info(team_id)
            if not team_info:
                return jsonify({'success': False, 'message': 'Tým nebyl nalezen.'}), 404
            team_name = team_info.get('team', {}).get('name', 'Unknown')
            team_logo = team_info.get('team', {}).get('logo', '')
        
        favorite = FavoriteTeam(
            user_id=current_user.id,
            team_id=team_id,
            team_name=team_name,
            team_logo=team_logo
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tým přidán do oblíbených.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Chyba při přidávání do oblíbených.'}), 500

@teams_bp.route('/<int:team_id>/favorite', methods=['DELETE'])
@login_required
def remove_favorite(team_id):
    """Remove team from favorites"""
    try:
        favorite = FavoriteTeam.query.filter_by(
            user_id=current_user.id,
            team_id=team_id
        ).first()
        
        if not favorite:
            return jsonify({'success': False, 'message': 'Tým není v oblíbených.'}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tým odebrán z oblíbených.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Chyba při odebírání z oblíbených.'}), 500
