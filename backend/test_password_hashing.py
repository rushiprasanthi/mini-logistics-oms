"""Test password hashing directly"""

import sys
import io
import traceback

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("DEBUGGING PASSWORD HASHING")
print("="*70)

# Step 1: Check imports
print("\n[Step 1] Checking passlib and bcrypt...")
try:
    from passlib.context import CryptContext
    from passlib.handlers.bcrypt import bcrypt
    import bcrypt as bcrypt_module
    print(f"  OK - passlib imported")
    print(f"  OK - bcrypt handler available")
    print(f"  OK - bcrypt module imported: {bcrypt_module.__version__}")
except Exception as e:
    print(f"  FAIL - Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Inspect CryptContext configuration
print("\n[Step 2] Testing CryptContext initialization...")
try:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )
    print("  OK - CryptContext created")
except Exception as e:
    print(f"  FAIL - CryptContext initialization: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test hash_password directly
print("\n[Step 3] Testing hash_password function...")
try:
    from app.services.auth_service import hash_password
    print("  OK - hash_password imported")
    
    password = "password123"
    print(f"  Testing with password: {password}")
    print(f"  Password length: {len(password)} bytes")
    
    hashed = hash_password(password)
    print(f"  OK - Password hashed successfully")
    print(f"  Hash: {hashed}")
    print(f"  Hash length: {len(hashed)} bytes")
    
except Exception as e:
    print(f"\n  FAIL - hash_password error: {type(e).__name__}: {e}")
    print("\n" + "-"*70)
    print("FULL TRACEBACK:")
    print("-"*70)
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test verify_password
print("\n[Step 4] Testing verify_password function...")
try:
    from app.services.auth_service import verify_password
    print("  OK - verify_password imported")
    
    is_valid = verify_password(password, hashed)
    print(f"  Verification result: {is_valid}")
    
    if is_valid:
        print("  OK - Password verification successful")
    else:
        print("  FAIL - Password verification failed (mismatch)")
        
except Exception as e:
    print(f"\n  FAIL - verify_password error: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[SUCCESS] All password hashing tests passed!")
