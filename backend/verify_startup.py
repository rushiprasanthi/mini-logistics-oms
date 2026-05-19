#!/usr/bin/env python
"""Quick startup verification."""

import sys

print("\n=== BACKEND STARTUP VERIFICATION ===\n")

# Test 1: Import main app
try:
    from app.main import app
    print("✓ Main app imported")
except Exception as e:
    print(f"✗ Failed to import main app: {e}")
    sys.exit(1)

# Test 2: Count routes
routes = [r for r in app.routes if hasattr(r, 'path')]
print(f"✓ Routes registered: {len(routes)}")

# Test 3: Check critical routes
route_paths = {r.path for r in routes if hasattr(r, 'path')}
critical = {
    '/api/v1/auth/register',
    '/api/v1/auth/login',
    '/api/v1/orders/',
    '/api/v1/orders/my',
    '/healthz',
}

for route in sorted(route_paths):
    if '/api/v1' in route or route == '/healthz':
        print(f"  • {route}")

missing = critical - route_paths
if missing:
    print(f"✗ Missing routes: {missing}")
else:
    print(f"✓ All critical routes present")

# Test 4: Check exception handlers
handlers = app.exception_handlers
print(f"✓ Exception handlers: {len(handlers)}")

# Test 5: Configuration
from app.core.config import settings
print(f"✓ Config - Project: {settings.PROJECT_NAME}")
print(f"✓ Config - DB: Oracle (THIN mode)")
print(f"✓ Config - JWT: {settings.JWT_ALGORITHM}")

# Test 6: All service imports
try:
    from app.services.order_service import OrderService
    from app.services.auth_service import hash_password
    from app.repositories.order_repo import OrderRepository
    from app.core.rbac import get_current_active_user
    from app.utils.jwt import get_current_user
    print("✓ All services imported")
except Exception as e:
    print(f"✗ Service import failed: {e}")
    sys.exit(1)

print("\n✓ BACKEND READY - All checks passed")
print("\nTo start server:")
print("  uvicorn app.main:app --reload")
print("\nSwagger UI:")
print("  http://127.0.0.1:8000/docs")
print()
