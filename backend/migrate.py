#!/usr/bin/env python
"""Database migration helper script for FootballVerse"""
import sys
import os
from alembic import command
from alembic.config import Config

def main():
    """Run database migrations"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini_path = os.path.join(script_dir, "alembic.ini")
    
    # Create Alembic config
    alembic_cfg = Config(alembic_ini_path)
    
    # Parse command
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "upgrade":
            print("Running database migrations...")
            command.upgrade(alembic_cfg, "head")
            print("✓ Migrations complete")
            
        elif cmd == "downgrade":
            print("Downgrading database by 1 revision...")
            command.downgrade(alembic_cfg, "-1")
            print("✓ Downgrade complete")
            
        elif cmd == "current":
            print("Current database revision:")
            command.current(alembic_cfg, verbose=True)
            
        elif cmd == "history":
            print("Migration history:")
            command.history(alembic_cfg)
            
        else:
            print(f"Unknown command: {cmd}")
            print_usage()
    else:
        print_usage()

def print_usage():
    print("""
Usage: python migrate.py [command]

Commands:
    upgrade    - Apply all pending migrations
    downgrade  - Revert the last migration
    current    - Show current database revision
    history    - Show migration history
""")

if __name__ == "__main__":
    main()
