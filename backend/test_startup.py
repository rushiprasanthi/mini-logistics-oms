#!/usr/bin/env python
"""
Comprehensive backend startup verification script.
Checks imports, routes, handlers, and configuration.
"""

import sys


def test_imports():
    """Test that all core modules import successfully."""
    print("\n=== Testing Imports ===")
    try:
        from app.main import app
        print("✓ app.main imported")
        
        from app.core.config import settings
        print("✓ app.core.config imported")
        
        from app.db.session import Base, engine, get_db
        print("✓ app.db.session imported")
        
        from app.core.rbac import get_current_active_user
        print("✓ app.core.rbac imported")
        
        from app.services.order_service import OrderService
        print("✓ app.services.order_service imported")
        
        from app.services.auth_service import hash_password
        print("✓ app.services.auth_service imported")
        
        from app.repositories.order_repo import OrderRepository
        print("✓ app.repositories.order_repo imported")
        
        return True, app
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False, None


def test_app_structure(app):
    """Test FastAPI app structure."""
    print("\n=== Testing App Structure ===")
    
    # Check routes
    routes = [r for r in app.routes if hasattr(r, 'path')]
    print(f"✓ Routes registered: {len(routes)} endpoints")
    
    # Check exception handlers
    handlers = app.exception_handlers
    print(f"✓ Exception handlers: {len(handlers)} handlers")
    
    # Verify required routes exist
    route_paths = {r.path for r in routes}
    required_routes = {
        '/api/v1/auth/register',
        '/api/v1/auth/login',
        '/api/v1/orders/',
        '/api/v1/orders/my',
        '/healthz',
    }
    
    missing = required_routes - route_paths
    if missing:
        print(f"✗ Missing routes: {missing}")
        return False
    
    print(f"✓ All required routes present")
    return True


def test_configuration():
    """Test configuration loading."""
    print("\n=== Testing Configuration ===")
    try:
        from app.core.config import settings
        
        assert settings.PROJECT_NAME == "mini-logistics-oms"
        print(f"✓ Project name: {settings.PROJECT_NAME}")
        
        assert settings.JWT_ALGORITHM == "HS256"
        print(f"✓ JWT algorithm: {settings.JWT_ALGORITHM}")
        
        assert "oracle+oracledb://" in settings.SQLALCHEMY_DATABASE_URI
        print("✓ Database URI configured for Oracle")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n=== Testing Schemas ===")
    try:
        from app.schemas.order import OrderCreate
        from app.schemas.user import UserCreate
        
        # Test order schema
        order = OrderCreate(external_id="TEST-001")
        print(f"✓ OrderCreate schema valid")
        
        # Test user schema
        user = UserCreate(email="test@example.com", password="password123")
        print(f"✓ UserCreate schema valid")
        
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False


def test_exception_handlers():
    """Test custom exception classes."""
    print("\n=== Testing Exception Handlers ===")
    try:
        from app.core.exceptions import (
            AppError,
            ValidationError,
            UnauthorizedError,
            ForbiddenError,
            NotFoundError,
            InvalidTransitionError,
            DuplicateError,
        )
        
        # Test exception instantiation
        exc = ValidationError("test error")
        assert exc.status_code == 422
        print("✓ ValidationError works")
        
        exc = UnauthorizedError("unauthorized")
        assert exc.status_code == 401
        print("✓ UnauthorizedError works")
        
        exc = ForbiddenError("forbidden")
        assert exc.status_code == 403
        print("✓ ForbiddenError works")
        
        exc = NotFoundError("not found")
        assert exc.status_code == 404
        print("✓ NotFoundError works")
        
        exc = InvalidTransitionError("PENDING", "DELIVERED")
        assert exc.status_code == 400
        print("✓ InvalidTransitionError works")
        
        return True
    except Exception as e:
        print(f"✗ Exception test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("BACKEND RUNTIME VERIFICATION")
    print("="*50)
    
    success, app = test_imports()
    if not success:
        print("\n✗ Import test failed")
        sys.exit(1)
    
    success = test_app_structure(app)
    if not success:
        print("\n✗ App structure test failed")
        sys.exit(1)
    
    success = test_configuration()
    if not success:
        print("\n✗ Configuration test failed")
        sys.exit(1)
    
    success = test_schemas()
    if not success:
        print("\n✗ Schema test failed")
        sys.exit(1)
    
    success = test_exception_handlers()
    if not success:
        print("\n✗ Exception handler test failed")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("✓ ALL TESTS PASSED - Backend is ready")
    print("="*50)
    print("\nTo start the backend:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print("\nThen visit:")
    print("  http://127.0.0.1:8000/docs (Swagger)")
    print("  http://127.0.0.1:8000/healthz (Health check)")
    print("="*50 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
