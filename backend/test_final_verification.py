"""Comprehensive test of register endpoint fix"""

import sys
import io
import json
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("FINAL VERIFICATION - REGISTER ENDPOINT")
print("="*70)

try:
    from app.main import create_app
    from app.db.session import engine, Base, create_sequences, SessionLocal
    from app.api.v1.auth import register
    from app.schemas.user import UserCreate
    
    # Setup
    print("\n[Setup] Initializing...")
    app = create_app()
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK")
    
    # Test 1: Register new user
    print("\n[Test 1] Registering new user...")
    session = SessionLocal()
    unique_id = int(time.time() * 1000) % 100000
    email = f"finaltest{unique_id}@example.com"
    
    payload = UserCreate(email=email, password="test@Pass123")
    result = register(payload=payload, db=session)
    session.close()
    
    if result.get("success"):
        print(f"  OK - Registration successful")
        print(f"    ID: {result['data']['id']}")
        print(f"    Email: {result['data']['email']}")
    else:
        print(f"  FAIL - {result}")
        sys.exit(1)
    
    # Test 2: Verify response is JSON-serializable
    print("\n[Test 2] JSON serialization...")
    json_str = json.dumps(result)
    print(f"  OK - Serialized ({len(json_str)} bytes)")
    
    # Test 3: Try duplicate registration
    print("\n[Test 3] Rejecting duplicate email...")
    session = SessionLocal()
    result = register(payload=payload, db=session)
    session.close()
    
    if not result.get("success") and result.get("code") == 409:
        print(f"  OK - Duplicate rejected with code 409")
    else:
        print(f"  FAIL - Expected 409 error, got: {result}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("SUCCESS - All tests passed!")
    print("="*70)
    
except Exception as e:
    print(f"\nFAIL - {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
