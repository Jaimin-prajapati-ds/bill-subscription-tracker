"""API endpoint tests using pytest."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_subscription_unauthorized():
    """Test creating subscription without authentication."""
    response = client.post("/subscriptions/", json={"name": "Test"})
    assert response.status_code == 401

def test_get_subscriptions_unauthorized():
    """Test getting subscriptions without authentication."""
    response = client.get("/subscriptions/")
    assert response.status_code == 401

def test_register_user():
    """Test user registration."""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code in [200, 201]

def test_login_user():
    """Test user login."""
    # First register
    client.post("/auth/register", json={
        "email": "login_test@example.com",
        "password": "testpass123"
    })
    # Then login
    response = client.post("/auth/login", json={
        "email": "login_test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    """Test login with invalid credentials."""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
