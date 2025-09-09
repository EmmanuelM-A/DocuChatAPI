# Development Usage

## Quick Links

- [Database Commands](#database-commands)
- [Initial Project Setup](#initial-project-setup-one-time)
- [During Active Development](#during-active-development)
- [Safe Operations (Server Running)](#safe-operations-server-running)
- [Potential Dangerous Operations](#potentially-dangerous-operations)
- [Common Development Scenarios](#common-development-scenarios)
- [Environment-Specific Usage](#environment-specific-usage)

---

## Database Commands

| Command                                    | Purpose                | Safe While Server Running? |
|--------------------------------------------|------------------------|----------------------------|
| `python manage.py db status`               | Check current state    | ✅ Yes                      |
| `python manage.py db history`              | View migration history | ✅ Yes                      |
| `python manage.py db migrate -m "message"` | Create new migration   | ✅ Yes                      |
| `python manage.py db upgrade`              | Apply migrations       | ⚠️ Brief locks             |
| `python manage.py db downgrade <rev>`      | Rollback migration     | ❌ Can break server         |
| `python manage.py db reset --confirm`      | Reset everything       | ❌ Will break server        |

---

## Initial Project Setup (One-time)

### 1. Start Docker Database

```bash
# Start the PostgresSQL database
docker-compose up postgres

# Or start all services in background
docker-compose up -d
```

### 2. Initialize The Database

This creates the migration infrastructure, database tables and initial seed data.

```bash
python manage.py db init
```

**What this does:**
- Creates migration directory structure
- Sets up Alembic configuration
- Creates all database tables
- Seeds initial data (plans, test user)
- Creates first migration file

### 3. Verify Setup

```bash
# Check that everything worked
python manage.py db status
```

You should see something like:
```
✅ Database is operational and ready
Current Migration: abc12345 (Initial database schema)  
Pending Migrations: No
```

---

## During Active Development

### When You Modify SQLAlchemy Models

```bash
# 1. After changing your models, create a migration
python manage.py db migrate -m "Add email verification to users"

# 2. Review the generated migration file in src/database/migrations/versions/

# 3. Apply the migration
python manage.py db upgrade
```

### Example Workflow: Adding a New Table

```bash
# 1. Create your new SQLAlchemy model in src/database/models/
# 2. Import it in src/database/models/__init__.py
# 3. Generate migration
python manage.py db migrate -m "Add document table"

# 4. Check the generated migration
ls src/database/migrations/versions/

# 5. Apply it
python manage.py db upgrade
```

---

## Safe Operations (Server Running)

These operations are safe to run while your FastAPI server is running:

| Operation            | Command                                | Notes                                   |
|----------------------|----------------------------------------|-----------------------------------------|
| **Check Status**     | `python manage.py db status`           | Read-only, no locks                     |
| **View History**     | `python manage.py db history`          | Read-only, no locks                     |
| **Create Migration** | `python manage.py db migrate -m "..."` | Only creates files, no DB changes       |
| **Apply Migration**  | `python manage.py db upgrade`          | Brief table locks during schema changes |

### Migration Locks Explained

When running `db upgrade` while server is running:

- **Brief locks** (< 1 second): Adding columns, indexes, constraints
- **Longer locks** (seconds to minutes): Major restructuring, data migrations
- **No locks**: Creating migration files

---

## Potentially Dangerous Operations

⚠️ **These can break your running server:**

| Command                               | Risk Level  | Why Dangerous                          |
|---------------------------------------|-------------|----------------------------------------|
| `python manage.py db downgrade -1`    | 🔴 High     | Removes columns/tables the app expects |
| `python manage.py db reset --confirm` | 🔴 Critical | Deletes all data and tables            |

---

## Common Development Scenarios

### 📝 Adding a New Feature

```bash
# 1. Modify your SQLAlchemy models
# 2. Create migration
python manage.py db migrate -m "Add document upload feature"

# 3. Review the generated migration file
cat src/database/migrations/versions/20240315_1420_*.py

# 4. Apply it
python manage.py db upgrade

# 5. Your server will now work with the new schema
```

### 🔄 Rolling Back Changes

```bash
# Check what migrations exist
python manage.py db history

# Rollback to previous migration
python manage.py db downgrade -1

# Or rollback to specific revision  
python manage.py db downgrade abc123
```

### 🔍 Checking Current State

```bash
# Detailed status with health checks
python manage.py db status

# Quick overview
python manage.py db status --quick

# Raw migration history
python manage.py db history
```

---

## Environment-Specific Usage

### 🏠 Local Development

```bash
# When you mess up locally and want to start fresh
python manage.py db reset --confirm
python manage.py db init

# Create test data
python manage.py db init  # Already includes test user

# Check what you have
python manage.py db status
```

### 🚀 Staging/Production

```bash
# ONLY run upgrades, never reset
python manage.py db upgrade

# Check status after deployment
python manage.py db status

# View recent migrations
python manage.py db history
```



