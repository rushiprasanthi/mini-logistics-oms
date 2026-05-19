"""Debug test for POST /api/v1/auth/register"""

import sys
import traceback
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import create_app


def test_register_endpoint():
    """Test the register endpoint and capture detailed error info"""
    app = create_app()
    client = TestClient(app)
    
    # Test data
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    print("\n" + "="*60)
    print("Testing POST /api/v1/auth/register")
    print("="*60)
    print(f"Payload: {payload}")
    
    try:
        response = client.post(
            "/api/v1/auth/register",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code != 201:
            print(f"ERROR: Expected 201, got {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    test_register_endpoint()
