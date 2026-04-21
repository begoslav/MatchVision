from .auth import auth_bp
from .main import main_bp
from .teams import teams_bp
from .matches import matches_bp
from .favorites import favorites_bp
from .players import players_bp

__all__ = ['auth_bp', 'main_bp', 'teams_bp', 'matches_bp', 'favorites_bp', 'players_bp']
