"""Test FastAPI response serialization"""

import sys
import io
import json
import traceback
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("TESTING FASTAPI RESPONSE SERIALIZATION")
print("="*70)

# Step 1: Setup
print("\n[Step 1] Setup...")
try:
    from app.main import create_app
    from app.db.session import engine, Base, get_db, create_sequences
    from app.repositories.user_repo import UserRepository
    from app.services.auth_service import hash_password
    from app.core.responses import success
    
    app = create_app()
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK - Setup complete")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Create a user
print("\n[Step 2] Creating user...")
try:
    session = next(get_db())
    repo = UserRepository(session)
    
    unique_id = int(time.time() * 1000) % 100000
    email = f"serialtest{unique_id}@example.com"
    
    user = repo.create(
        email=email,
        hashed_password=hash_password("password123")
    )
    session.commit()
    print(f"  OK - User created: ID={user.id}")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Build response dict (as auth.py does)
print("\n[Step 3] Building response dict...")
try:
    response_dict = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    
    print(f"  Response dict built:")
    for key, value in response_dict.items():
        print(f"    {key}: {value} (type: {type(value).__name__})")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Call success() function
print("\n[Step 4] Calling success() function...")
try:
    success_response = success(
        response_dict,
        message="user_registered",
    )
    
    print(f"  OK - Success response built")
    print(f"  Response keys: {list(success_response.keys())}")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 5: JSON serialization (what FastAPI does)
print("\n[Step 5] JSON serialization...")
try:
    json_str = json.dumps(success_response)
    print(f"  OK - JSON serialized")
    print(f"  JSON length: {len(json_str)} bytes")
    
    parsed = json.loads(json_str)
    print(f"  OK - JSON parsed back")
    
except Exception as e:
    print(f"  FAIL - {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 6: Check for ORM object references (common serialization issue)
print("\n[Step 6] Checking for non-serializable objects...")
try:
    import inspect
    
    def check_serializable(obj, path=""):
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return True
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if not check_serializable(v, f"{path}.{k}"):
                    return False
            return True
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                if not check_serializable(v, f"{path}[{i}]"):
                    return False
            return True
        else:
            # Non-primitive type
            print(f"    WARNING: Non-serializable at {path}: {type(obj).__name__}")
            return False
    
    if check_serializable(success_response):
        print(f"  OK - All objects are JSON-serializable")
    else:
        print(f"  FAIL - Found non-serializable objects")
        sys.exit(1)
    
except Exception as e:
    print(f"  Error during check: {e}")

# Step 7: Test with TestClient
print("\n[Step 7] Testing with FastAPI TestClient...")
try:
    from starlette.testclient import TestClient
    
    client = TestClient(app)
    
    unique_id2 = int(time.time() * 1000) % 100000
    payload = {
        "email": f"testhttp{unique_id2}@example.com",
        "password": "password123"
    }
    
    print(f"  POSTing to /api/v1/auth/register...")
    response = client.post(
        "/api/v1/auth/register",
        json=payload
    )
    
    print(f"  Status code: {response.status_code}")
    print(f"  Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"  OK - Request successful")
        print(f"  Response: {response.json()}")
    else:
        print(f"  FAIL - Unexpected status: {response.status_code}")
        print(f"  Response: {response.text}")
        
except Exception as e:
    print(f"  FAIL - {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
finally:
    session.close()

print("\n[SUCCESS] Response serialization test complete!")
