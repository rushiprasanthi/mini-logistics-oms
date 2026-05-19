"""Detailed password hashing diagnostics"""

import sys
import io
import traceback

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*70)
print("PASSWORD HASHING DIAGNOSTICS")
print("="*70)

# Section 1: Environment inspection
print("\n[Section 1] Package Versions")
print("-"*70)

try:
    import passlib
    print(f"passlib version: {passlib.__version__}")
except:
    print("passlib version: (not found)")

try:
    import bcrypt
    print(f"bcrypt version: {bcrypt.__version__}")
except:
    print("bcrypt version: (not found)")

# Section 2: CryptContext inspection
print("\n[Section 2] CryptContext Configuration")
print("-"*70)

try:
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )
    
    print(f"Configured schemes: {pwd_context.schemes()}")
    print(f"Default scheme: {pwd_context.default_scheme()}")
    
    # Try to get handler info
    bcrypt_handler = pwd_context.identify("$2b$12$test")
    print(f"BCrypt handler available: {bcrypt_handler is not None}")
    
except Exception as e:
    print(f"CryptContext error: {e}")
    traceback.print_exc()

# Section 3: Hash function inspection
print("\n[Section 3] hash_password() Function")
print("-"*70)

try:
    from app.services.auth_service import hash_password, verify_password
    import inspect
    
    print("hash_password source:")
    print(inspect.getsource(hash_password))
    
    print("\nverify_password source:")
    print(inspect.getsource(verify_password))
    
except Exception as e:
    print(f"Error inspecting functions: {e}")
    traceback.print_exc()

# Section 4: Functional test
print("\n[Section 4] Functional Test")
print("-"*70)

test_passwords = [
    "password123",
    "P@ssw0rd!",
    "short",
    "a" * 72,  # Exactly 72 bytes (bcrypt limit)
    "a" * 100,  # Over 72 bytes
]

for test_pwd in test_passwords:
    try:
        hashed = hash_password(test_pwd)
        is_valid = verify_password(test_pwd, hashed)
        
        status = "OK" if is_valid else "FAIL"
        print(f"[{status}] len={len(test_pwd):3d} | {test_pwd[:30]:<30} | {hashed[:30]}")
        
    except Exception as e:
        print(f"[ERROR] len={len(test_pwd):3d} | {test_pwd[:30]:<30} | {type(e).__name__}: {str(e)[:40]}")

print("\n" + "="*70)
print("DIAGNOSTICS COMPLETE")
print("="*70)
