"""Test the complete register flow to identify HTTP 500"""

import sys
import io
import traceback

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("TESTING COMPLETE REGISTER FLOW")
print("="*70)

# Step 1: Setup
print("\n[Step 1] Setting up app and database...")
try:
    from app.main import create_app
    from app.db.session import engine, Base, get_db, create_sequences
    from sqlalchemy import text
    
    app = create_app()
    print("  OK - App created")
    
    # Create tables and sequences
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK - Tables and sequences ready")
    
except Exception as e:
    print(f"  FAIL - Setup error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Get DB session
print("\n[Step 2] Getting database session...")
try:
    session = next(get_db())
    print("  OK - Session obtained")
except Exception as e:
    print(f"  FAIL - Session error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test UserRepository.create
print("\n[Step 3] Testing UserRepository.create()...")
try:
    from app.repositories.user_repo import UserRepository
    from app.services.auth_service import hash_password
    
    repo = UserRepository(session)
    email = "testuser@example.com"
    password = "securepass123"
    
    print(f"  Creating user: {email}")
    print(f"  Password: {password}")
    
    hashed = hash_password(password)
    print(f"  Hashed password generated: {hashed[:20]}...")
    
    user = repo.create(
        email=email,
        hashed_password=hashed
    )
    
    print(f"  OK - User created")
    print(f"    ID: {user.id}")
    print(f"    Email: {user.email}")
    print(f"    Role: {user.role}")
    print(f"    Is Active: {user.is_active}")
    
except Exception as e:
    print(f"\n  FAIL - Repository error: {type(e).__name__}: {e}")
    print("\n" + "-"*70)
    print("FULL TRACEBACK:")
    print("-"*70)
    traceback.print_exc()
    sys.exit(1)

# Step 4: Commit transaction
print("\n[Step 4] Committing transaction...")
try:
    session.commit()
    print("  OK - Committed")
except Exception as e:
    print(f"\n  FAIL - Commit error: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 5: Test response object building
print("\n[Step 5] Building response object...")
try:
    response_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    print("  OK - Response object built")
    print(f"    {response_data}")
except Exception as e:
    print(f"\n  FAIL - Response building error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 6: Test success response function
print("\n[Step 6] Testing success response function...")
try:
    from app.core.responses import success
    
    result = success(
        response_data,
        message="user_registered",
    )
    print("  OK - Success response built")
    print(f"    Status: {result.status_code}")
except Exception as e:
    print(f"\n  FAIL - Success response error: {e}")
    traceback.print_exc()
    sys.exit(1)

session.close()
print("\n[SUCCESS] Complete register flow test passed!")
