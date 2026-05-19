"""Direct test to capture register endpoint error with line numbers"""

import traceback
import sys
import logging
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

print("\n" + "="*70)
print("DEBUGGING POST /api/v1/auth/register")
print("="*70)

# Step 1: Import app
print("\n[Step 1] Creating app...")
try:
    from app.main import create_app
    app = create_app()
    print("  OK - App created successfully")
except Exception as e:
    print(f"  FAIL - Failed to create app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Test with direct call simulation
print("\n[Step 2] Testing register endpoint directly...")
try:
    from app.core.config import settings
    from app.db.session import get_db, engine, Base
    from app.repositories.user_repo import UserRepository
    from app.services.auth_service import hash_password
    from app.models.user import User
    from app.schemas.user import UserCreate
    from sqlalchemy.orm import Session
    
    print("  OK - All imports successful")
    
    # Create tables
    print("\n[Step 3] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("  OK - Tables created/verified")
    
    # Create sequences
    print("\n[Step 3b] Creating database sequences...")
    from app.db.session import create_sequences
    create_sequences()
    print("  OK - Sequences created/verified")
    
    # Get session
    print("\n[Step 4] Getting database session...")
    session = next(get_db())
    print("  OK - Session obtained")
    
    # Create user
    print("\n[Step 5] Creating user via repository...")
    email = "test@example.com"
    password = "password123"
    repo = UserRepository(session)
    
    print(f"  - Email: {email}")
    print(f"  - Password: {password}")
    
    user = repo.create(
        email=email,
        hashed_password=hash_password(password)
    )
    print(f"  OK - User created with ID: {user.id}")
    print(f"    Email: {user.email}")
    print(f"    Role: {user.role}")
    print(f"    Is Active: {user.is_active}")
    
    # Commit
    print("\n[Step 6] Committing transaction...")
    session.commit()
    print("  OK - Transaction committed")
    
    session.close()
    print("\n[SUCCESS] All steps completed successfully!")
    
except Exception as e:
    print(f"\n  FAIL - Error: {type(e).__name__}: {e}")
    print("\n" + "-"*70)
    print("FULL TRACEBACK:")
    print("-"*70)
    traceback.print_exc()
