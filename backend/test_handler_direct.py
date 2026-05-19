"""Test auth register handler directly"""

import sys
import io
import json
import traceback
import time
from unittest.mock import MagicMock

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("TESTING AUTH REGISTER HANDLER DIRECTLY")
print("="*70)

# Step 1: Setup
print("\n[Step 1] Setup...")
try:
    from app.main import create_app
    from app.db.session import engine, Base, get_db, create_sequences
    from app.api.v1.auth import register
    from app.schemas.user import UserCreate
    
    app = create_app()
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK - Setup complete")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Call register handler directly
print("\n[Step 2] Calling register handler...")
try:
    from app.db.session import SessionLocal
    session = SessionLocal()
    
    unique_id = int(time.time() * 1000) % 100000
    email = f"directtest{unique_id}@example.com"
    
    # Create payload
    payload = UserCreate(
        email=email,
        password="password123"
    )
    
    print(f"  Payload: email={email}, password=password123")
    
    # Call handler
    result = register(payload=payload, db=session)
    
    print(f"  OK - Handler returned")
    print(f"  Result type: {type(result).__name__}")
    print(f"  Result: {result}")
    
    # Try to JSON serialize the result
    print("\n[Step 3] JSON serialization...")
    try:
        json_str = json.dumps(result)
        print(f"  OK - Serialized to JSON")
        print(f"  JSON: {json_str[:100]}...")
    except Exception as e:
        print(f"  FAIL - JSON serialization failed: {type(e).__name__}: {e}")
        traceback.print_exc()
    
except Exception as e:
    print(f"  FAIL - Handler error: {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
finally:
    session.close()

print("\n[DONE] Direct handler test complete")
