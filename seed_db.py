#!/usr/bin/env python
"""
Seed database with demo data
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.models import db, User, FavoriteTeam

def seed_database():
    """Seed database with demo data"""
    load_dotenv()
    app = create_app()
    
    with app.app_context():
        print("Seedování databáze...")
        
        # Create demo user
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            demo_user = User(
                username='demo',
                email='demo@matchvision.com'
            )
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Demo uživatel vytvořen (demo / demo123)")
        
        # Add some favorite teams (demo IDs from API-Football)
        # Manchester United = 33, Liverpool = 40, Bayern Munich = 25
        demo_teams = [
            {'team_id': 33, 'team_name': 'Manchester United', 'team_logo': 'https://media.api-football.com/teams/33.png'},
            {'team_id': 40, 'team_name': 'Liverpool', 'team_logo': 'https://media.api-football.com/teams/40.png'},
            {'team_id': 25, 'team_name': 'Bayern Munich', 'team_logo': 'https://media.api-football.com/teams/25.png'},
        ]
        
        for team_data in demo_teams:
            existing = FavoriteTeam.query.filter_by(
                user_id=demo_user.id,
                team_id=team_data['team_id']
            ).first()
            
            if not existing:
                favorite = FavoriteTeam(
                    user_id=demo_user.id,
                    team_id=team_data['team_id'],
                    team_name=team_data['team_name'],
                    team_logo=team_data['team_logo']
                )
                db.session.add(favorite)
        
        db.session.commit()
        print("✅ Demo data přidána")
        
        # Print summary
        total_users = User.query.count()
        total_favorites = FavoriteTeam.query.count()
        print(f"\nShrnutí:")
        print(f"  - Uživatelů: {total_users}")
        print(f"  - Oblíbených týmů: {total_favorites}")

if __name__ == '__main__':
    seed_database()
