#!/usr/bin/env python
"""
Test script to verify the application
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.models import db, User, FavoriteTeam

def test_app():
    """Test application setup"""
    load_dotenv()
    
    print("=" * 50)
    print("MatchVision - Test kontrola")
    print("=" * 50)
    
    # Create app
    print("\n1. Vytváření aplikace...")
    try:
        app = create_app()
        print("   ✅ Aplikace vytvořena")
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
        return False
    
    # Check configuration
    print("\n2. Kontrola konfigurace...")
    with app.app_context():
        print(f"   - FLASK_ENV: {app.config.get('ENV', 'N/A')}")
        print(f"   - DEBUG: {app.debug}")
        print(f"   - DATABASE: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"   - API_KEY: {'✅ Nastaveno' if app.config.get('API_FOOTBALL_KEY') else '⚠️  Není nastaveno'}")
    
    # Test database
    print("\n3. Kontrola databáze...")
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   ✅ Databáze připravena ({len(tables)} tabulek)")
            for table in tables:
                print(f"      - {table}")
        except Exception as e:
            print(f"   ❌ Chyba databáze: {e}")
            return False
    
    # Test user creation
    print("\n4. Testování user modelu...")
    with app.app_context():
        try:
            # Check if test user exists
            test_user = User.query.filter_by(username='test_user').first()
            if not test_user:
                test_user = User(username='test_user', email='test@example.com')
                test_user.set_password('test_password')
                db.session.add(test_user)
                db.session.commit()
                print("   ✅ Testovací uživatel vytvořen")
            else:
                print("   ℹ️  Testovací uživatel již existuje")
            
            # Verify password
            if test_user.check_password('test_password'):
                print("   ✅ Ověření hesla funguje")
            
        except Exception as e:
            print(f"   ❌ Chyba: {e}")
            return False
    
    # Test API service
    print("\n5. Kontrola API service...")
    try:
        from app.services import api_service
        print("   ✅ API service importován")
        if api_service.api_key:
            print("   ✅ API klíč je nastaven")
        else:
            print("   ⚠️  API klíč není nastaven (získaná data budou omezena)")
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
        return False
    
    # Test Summary service
    print("\n6. Kontrola Summary service...")
    try:
        from app.services import summary_service
        print("   ✅ Summary service importován")
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
        return False
    
    # Test blueprints
    print("\n7. Kontrola blueprintů...")
    with app.app_context():
        blueprints = app.blueprints
        print(f"   Registrované blueprinty: {len(blueprints)}")
        for bp_name in blueprints:
            print(f"      - {bp_name}")
    
    print("\n" + "=" * 50)
    print("✅ Všechny testy prošly!")
    print("=" * 50)
    print("\nAplikace je připravena k použití.")
    print("Spusťte: python run.py\n")
    
    return True

if __name__ == '__main__':
    success = test_app()
    exit(0 if success else 1)
