#!/usr/bin/env python
"""
Database initialization script
Vytvoří databázi a všechny tabulky
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.models import db

def init_db():
    """Initialize the database"""
    load_dotenv()
    app = create_app()
    
    with app.app_context():
        print("Vytvářím databázi...")
        db.create_all()
        print("✅ Databáze vytvořena úspěšně!")
        
        # Print tables info
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nVytvořené tabulky: {len(tables)}")
        for table in tables:
            print(f"  - {table}")

if __name__ == '__main__':
    init_db()
