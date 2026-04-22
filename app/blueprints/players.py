from flask import Blueprint, render_template
from app.services import api_service

players_bp = Blueprint('players', __name__, url_prefix='/players')


@players_bp.route('/<int:player_id>')
def profile(player_id):
    """Player profile page with season stats and recent matches."""
    player_data = api_service.get_player_profile(player_id)
    recent_fixtures = api_service.get_player_recent_fixtures(player_id)

    return render_template(
        'players/profile.html',
        player_data=player_data,
        recent_fixtures=recent_fixtures,
        player_id=player_id,
    )


@players_bp.route('/<int:player_id>/transfers')
def transfers(player_id):
    """Player transfer history page."""
    player_data = api_service.get_player_profile(player_id)
    transfer_list = api_service.get_player_transfers(player_id)

    return render_template(
        'players/transfers.html',
        player_data=player_data,
        transfers=transfer_list,
        player_id=player_id,
    )
