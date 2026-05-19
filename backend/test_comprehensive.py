#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comprehensive backend runtime and functionality validation."""

import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_core_imports():
    """Test all core module imports."""
    print("\n=== TEST 1: Core Imports ===")
    modules = [
        ('app.main', 'FastAPI app'),
        ('app.core.config', 'Configuration'),
        ('app.db.session', 'Database session'),
        ('app.core.rbac', 'RBAC/auth'),
        ('app.services.order_service', 'Order service'),
        ('app.services.auth_service', 'Auth service'),
        ('app.services.audit_service', 'Audit service'),
        ('app.repositories.order_repo', 'Order repository'),
        ('app.repositories.user_repo', 'User repository'),
        ('app.repositories.audit_repo', 'Audit repository'),
        ('app.models.order', 'Order model'),
        ('app.models.user', 'User model'),
        ('app.models.order_event', 'OrderEvent model'),
        ('app.utils.jwt', 'JWT utilities'),
        ('app.core.exceptions', 'Exception classes'),
        ('app.core.responses', 'Response helpers'),
    ]
    
    for module_name, desc in modules:
        try:
            __import__(module_name)
            print(f"  [OK] {desc}")
        except Exception as e:
            print(f"  [FAIL] {desc}: {e}")
            return False
    
    return True


def test_app_structure():
    """Test FastAPI app structure and routes."""
    print("\n=== TEST 2: App Structure ===")
    try:
        from app.main import app
        
        routes = [r for r in app.routes if hasattr(r, 'path')]
        print(f"  [OK] Routes registered: {len(routes)} endpoints")
        
        handlers = app.exception_handlers
        print(f"  [OK] Exception handlers: {len(handlers)} registered")
        
        critical_routes = {
            '/api/v1/auth/register',
            '/api/v1/auth/login',
            '/api/v1/orders/',
            '/api/v1/orders/my',
            '/api/v1/orders/{order_id}/status/{target_status}',
            '/healthz',
        }
        
        actual_routes = {r.path for r in routes if hasattr(r, 'path')}
        missing = critical_routes - actual_routes
        
        if missing:
            print(f"  [FAIL] Missing routes: {missing}")
            return False
        
        print(f"  [OK] All {len(critical_routes)} critical routes present")
        return True
        
    except Exception as e:
        print(f"  [FAIL] App structure test failed: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\n=== TEST 3: Configuration ===")
    try:
        from app.core.config import settings
        
        checks = [
            ('Project name', settings.PROJECT_NAME == 'mini-logistics-oms'),
            ('JWT algorithm', settings.JWT_ALGORITHM == 'HS256'),
            ('Oracle THIN URL', 'oracle+oracledb://' in settings.SQLALCHEMY_DATABASE_URI),
            ('Access token expiry', settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0),
        ]
        
        for check_name, result in checks:
            if result:
                print(f"  [OK] {check_name}")
            else:
                print(f"  [FAIL] {check_name}")
                return False
        
        print(f"  [OK] DB URI configured correctly")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Configuration test failed: {e}")
        return False


def test_transaction_patterns():
    """Test that repositories follow flush-only pattern."""
    print("\n=== TEST 4: Transaction Patterns ===")
    try:
        import inspect
        from app.repositories import order_repo, user_repo, audit_repo
        
        repos = [
            ('OrderRepository.create', order_repo.OrderRepository.create),
            ('OrderRepository.update_status', order_repo.OrderRepository.update_status),
            ('UserRepository.create', user_repo.UserRepository.create),
            ('AuditRepository.create_event', audit_repo.AuditRepository.create_event),
        ]
        
        for repo_method, method in repos:
            source = inspect.getsource(method)
            
            if 'flush' not in source:
                print(f"  [FAIL] {repo_method} missing flush()")
                return False
            
            if 'commit()' in source and '.commit()' in source:
                print(f"  [FAIL] {repo_method} contains commit()")
                return False
            
            print(f"  [OK] {repo_method} uses flush-only pattern")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Transaction pattern test failed: {e}")
        return False


def test_rbac_and_security():
    """Test RBAC and security functions."""
    print("\n=== TEST 5: RBAC & Security ===")
    try:
        from app.core.rbac import get_current_active_user, require_role
        from app.utils.jwt import decode_token, create_access_token
        from app.services.auth_service import hash_password, verify_password
        
        pwd = "test_password_123"
        hashed = hash_password(pwd)
        verified = verify_password(pwd, hashed)
        
        if not verified:
            print(f"  [FAIL] Password verification failed")
            return False
        print(f"  [OK] Password hashing and verification")
        
        token = create_access_token("test_user_1")
        decoded = decode_token(token)
        
        if decoded.get('sub') != "test_user_1":
            print(f"  [FAIL] JWT encode/decode failed")
            return False
        print(f"  [OK] JWT encode/decode")
        
        if not callable(get_current_active_user):
            print(f"  [FAIL] get_current_active_user not callable")
            return False
        print(f"  [OK] RBAC functions")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] RBAC/Security test failed: {e}")
        return False


def test_exception_handling():
    """Test custom exception classes."""
    print("\n=== TEST 6: Exception Handling ===")
    try:
        from app.core.exceptions import (
            AppError,
            ValidationError,
            UnauthorizedError,
            ForbiddenError,
            NotFoundError,
            ConflictError,
            InvalidTransitionError,
        )
        
        exceptions = [
            ('AppError', AppError),
            ('ValidationError', ValidationError),
            ('UnauthorizedError', UnauthorizedError),
            ('ForbiddenError', ForbiddenError),
            ('NotFoundError', NotFoundError),
            ('ConflictError', ConflictError),
            ('InvalidTransitionError', InvalidTransitionError),
        ]
        
        for exc_name, exc_class in exceptions:
            if not issubclass(exc_class, Exception):
                print(f"  [FAIL] {exc_name} not an Exception")
                return False
            
            if 'Transition' in exc_name:
                inst = exc_class('PENDING', 'CANCELLED')
            else:
                inst = exc_class()
            
            if not hasattr(inst, 'status_code'):
                print(f"  [FAIL] {exc_name} missing status_code")
                return False
            
            print(f"  [OK] {exc_name}")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Exception handling test failed: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n=== TEST 7: Schemas ===")
    try:
        from app.schemas.order import OrderCreate
        from app.schemas.user import UserCreate
        from app.core.responses import success, error, paginated
        
        order_data = OrderCreate(external_id="ORD-123456")
        if order_data.external_id != "ORD-123456":
            print(f"  [FAIL] OrderCreate validation failed")
            return False
        print(f"  [OK] OrderCreate schema")
        
        user_data = UserCreate(
            email="test@example.com",
            password="password123"
        )
        if user_data.email != "test@example.com":
            print(f"  [FAIL] UserCreate validation failed")
            return False
        print(f"  [OK] UserCreate schema")
        
        resp = success({"id": 1}, message="created")
        if not resp.get('success'):
            print(f"  [FAIL] success() response format")
            return False
        print(f"  [OK] Response helpers")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Schemas test failed: {e}")
        return False


def test_database_models():
    """Test SQLAlchemy models."""
    print("\n=== TEST 8: Database Models ===")
    try:
        from app.models.user import User
        from app.models.order import Order, OrderStatus
        from app.models.order_event import OrderStatusEvent
        from app.db.session import Base
        
        models = [
            ('User', User, ['id', 'email', 'hashed_password', 'is_active', 'role']),
            ('Order', Order, ['id', 'external_id', 'status', 'customer_id']),
            ('OrderStatusEvent', OrderStatusEvent, ['id', 'order_id', 'from_status', 'to_status']),
        ]
        
        for model_name, model_class, required_attrs in models:
            for attr in required_attrs:
                if not hasattr(model_class, attr):
                    print(f"  [FAIL] {model_name} missing {attr}")
                    return False
            print(f"  [OK] {model_name} model")
        
        if not hasattr(OrderStatus, 'PENDING'):
            print(f"  [FAIL] OrderStatus enum incomplete")
            return False
        print(f"  [OK] OrderStatus enum")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Database models test failed: {e}")
        return False


def test_service_layer():
    """Test service layer classes."""
    print("\n=== TEST 9: Service Layer ===")
    try:
        from app.services.order_service import OrderService
        from app.services.auth_service import hash_password
        from app.services.audit_service import AuditService
        
        required_methods = [
            'create_order',
            'get_order',
            'list_orders_for_owner',
            'transition',
        ]
        
        for method in required_methods:
            if not hasattr(OrderService, method):
                print(f"  [FAIL] OrderService missing {method}")
                return False
        print(f"  [OK] OrderService methods")
        
        if not hasattr(OrderService, 'ALLOWED_TRANSITIONS'):
            print(f"  [FAIL] OrderService missing ALLOWED_TRANSITIONS")
            return False
        print(f"  [OK] FSM transitions defined")
        
        if not callable(hash_password):
            print(f"  [FAIL] hash_password not callable")
            return False
        print(f"  [OK] Auth functions")
        
        if not hasattr(AuditService, 'record_order_transition'):
            print(f"  [FAIL] AuditService missing record_order_transition")
            return False
        print(f"  [OK] Audit service")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Service layer test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("BACKEND COMPREHENSIVE VALIDATION")
    print("="*60)
    
    tests = [
        test_core_imports,
        test_app_structure,
        test_configuration,
        test_transaction_patterns,
        test_rbac_and_security,
        test_exception_handling,
        test_schemas,
        test_database_models,
        test_service_layer,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"\n[FAIL] Test {test_func.__name__} crashed: {e}")
            results.append((test_func.__name__, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED - Backend ready for deployment")
        print("\nTo start server:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        print("\nSwagger UI: http://127.0.0.1:8000/docs")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
