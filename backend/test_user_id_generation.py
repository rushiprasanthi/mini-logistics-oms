"""Test User.id auto-generation with Oracle"""

import sys
import io
import traceback
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("TESTING USER.ID ORACLE AUTO-GENERATION")
print("="*70)

# Step 1: Setup
print("\n[Step 1] Setup app and database...")
try:
    from app.main import create_app
    from app.db.session import engine, Base, get_db, create_sequences
    
    app = create_app()
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK - App and DB ready")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Inspect User model
print("\n[Step 2] Inspecting User model...")
try:
    from app.models.user import User
    import inspect
    
    # Get column info
    id_column = User.__table__.columns['id']
    print(f"  Column name: {id_column.name}")
    print(f"  Column type: {id_column.type}")
    print(f"  Primary key: {id_column.primary_key}")
    print(f"  Autoincrement: {id_column.autoincrement}")
    print(f"  Server default: {id_column.server_default}")
    print(f"  Default: {id_column.default}")
    
    # Check for sequence
    if hasattr(id_column, 'sequences'):
        print(f"  Sequences: {id_column.sequences}")
    
    print("  OK - Model inspected")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()

# Step 3: Test user creation
print("\n[Step 3] Creating user with auto-generated ID...")
try:
    from app.repositories.user_repo import UserRepository
    from app.services.auth_service import hash_password
    
    session = next(get_db())
    repo = UserRepository(session)
    
    # Use unique email with timestamp
    unique_id = int(time.time() * 1000) % 100000
    email = f"testuser{unique_id}@example.com"
    password = "securepass123"
    
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    
    # Create user
    hashed = hash_password(password)
    user = repo.create(
        email=email,
        hashed_password=hashed
    )
    
    print(f"  OK - User object created")
    print(f"    user.id = {user.id}")
    print(f"    user.email = {user.email}")
    print(f"    user.role = {user.role}")
    print(f"    user.is_active = {user.is_active}")
    
    # Check if ID is set
    if user.id is None:
        print(f"  FAIL - user.id is None (not auto-generated)")
        sys.exit(1)
    else:
        print(f"  OK - ID auto-generated: {user.id}")
    
except Exception as e:
    print(f"\n  FAIL - {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Commit and verify
print("\n[Step 4] Committing and verifying...")
try:
    session.commit()
    print(f"  OK - Transaction committed")
    
    # Verify by querying back
    retrieved = repo.get(user.id)
    if retrieved:
        print(f"  OK - User retrieved by ID: {retrieved.id}")
    else:
        print(f"  FAIL - User not found by ID")
        
except Exception as e:
    print(f"\n  FAIL - {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
finally:
    session.close()

print("\n[SUCCESS] Oracle User.id auto-generation is working!")
