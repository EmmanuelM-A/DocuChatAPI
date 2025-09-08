"""
Main entry point for the application.
"""

from dotenv import load_dotenv
import uvicorn

from src.app import create_app

"""
Initial Project Setup (One-time)
After starting your Docker database but before starting your server for the first time:
bash# Start your database
docker-compose up postgres

# Initialize everything
python manage.py db init
This creates the migration infrastructure, database tables, and initial seed data.
2. During Active Development
When you modify your SQLAlchemy models, you need to create and apply migrations:
bash# After changing models, create a migration
python manage.py db migrate -m "Add email verification to users"

# Apply the migration
python manage.py db upgrade
3. Safe Usage While Server is Running
Most operations are safe to run while your server is running:
Safe operations:

python manage.py db status - Just reads current state
python manage.py db history - Just reads migration history
python manage.py db upgrade - Applies schema changes (brief locks)
python manage.py db migrate - Creates migration files (no DB changes)

Potentially problematic:

python manage.py db downgrade - Can break running server if it removes columns/tables the app expects
python manage.py db reset --confirm - Will definitely break your running server

4. Production Deployment
In production, you'd typically run migrations during deployment:
bash# In your deployment script
python manage.py db upgrade  # Apply any pending migrations
python start_server.py       # Then start the server
Typical Development Scenarios
Adding a New Feature
bash# 1. Modify your SQLAlchemy models
# 2. Create migration
python manage.py db migrate -m "Add document upload feature"

# 3. Review the generated migration file
# 4. Apply it
python manage.py db upgrade

# 5. Your server will now work with the new schema
Rolling Back Changes
bash# Check what migrations exist
python manage.py db history

# Rollback to previous migration
python manage.py db downgrade -1

# Or rollback to specific revision
python manage.py db downgrade abc123
Checking Current State
bash# See current migration status
python manage.py db status

# See full migration history
python manage.py db history
Database Locking Considerations
When you run migrations while the server is running:
Brief locks occur during:

Adding/dropping columns
Creating/dropping indexes
Adding constraints

Longer locks during:

Major table restructuring
Large data migrations

For production, consider:
bash# Stop server, migrate, restart (safest)
systemctl stop myapp
python manage.py db upgrade
systemctl start myapp
Environment-Specific Usage
Local Development
bash# Reset everything when you mess up locally
python manage.py db reset --confirm

# Re-initialize
python manage.py db init
Staging/Production
bash# Only run upgrades, never reset
python manage.py db upgrade

# Check status
python manage.py db status
"""


load_dotenv(".env")

app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="127.0.0.1", port=5000, reload=True)
