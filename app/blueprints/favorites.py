from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import FavoriteTeam

favorites_bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@favorites_bp.route('/')
@login_required
def list_favorites():
    """List user's favorite teams"""
    favorites = FavoriteTeam.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites)

@favorites_bp.route('/api')
@login_required
def api_favorites():
    """API endpoint for user's favorites"""
    favorites = FavoriteTeam.query.filter_by(user_id=current_user.id).all()
    data = [
        {
            'id': f.id,
            'team_id': f.team_id,
            'team_name': f.team_name,
            'team_logo': f.team_logo,
            'added_at': f.added_at.isoformat()
        }
        for f in favorites
    ]
    return jsonify({'success': True, 'favorites': data})
