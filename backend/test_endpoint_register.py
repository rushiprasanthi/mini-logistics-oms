"""Test register endpoint directly"""

import sys
import io
import json
import traceback
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("TESTING /api/v1/auth/register ENDPOINT")
print("="*70)

# Step 1: Create app
print("\n[Step 1] Creating FastAPI app...")
try:
    from app.main import create_app
    from app.db.session import engine, Base, create_sequences
    
    app = create_app()
    Base.metadata.create_all(bind=engine)
    create_sequences()
    print("  OK - App ready")
    
except Exception as e:
    print(f"  FAIL - {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Test with HTTPClient (avoiding TestClient issues)
print("\n[Step 2] Testing with httpx.Client...")
try:
    from httpx import Client
    
    client = Client(app=app, base_url="http://test")
    
    unique_id = int(time.time() * 1000) % 100000
    payload = {
        "email": f"httpxtest{unique_id}@example.com",
        "password": "password123"
    }
    
    print(f"  Payload: {payload}")
    print(f"  POSTing to /api/v1/auth/register...")
    
    response = client.post(
        "/api/v1/auth/register",
        json=payload
    )
    
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"  OK - Success response")
        try:
            data = response.json()
            print(f"  Response JSON: {json.dumps(data, indent=2)}")
        except Exception as e:
            print(f"  ERROR parsing JSON: {e}")
            print(f"  Raw text: {response.text}")
    else:
        print(f"  Status: {response.status_code}")
        print(f"  Response text: {response.text}")
        
except Exception as e:
    print(f"  FAIL - {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n[DONE] Endpoint test complete")
